#!/usr/bin/env python
import discord
from yapsy.PluginManager import PluginManager
from plugin import Plugin
import os
import logging
import urllib.request
import inspect
import commands
import botcommands

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

# Plugin Command dictionary and decorator
plugincommand = commands._loadCommands()

# Bot Command dictionary and decorator
botcommand = commands._loadCommands()

class Bot(discord.Client):
    
    def __init__(self):
        super().__init__()

        self.settingsChannelName = 'botsettings' # change this if you want your bot settings channel to have a different name
        self.voiceChannel = None
        self.voiceStarter = None

        self.botCommands = botcommands.BotCommands()

        # Setup logging for Discord.py
        self.discordLogger = logging.getLogger('discord')
        self.discordLogger.setLevel(logging.DEBUG)
        self.discordHandler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        self.discordHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))
        self.discordLogger.addHandler(self.discordHandler)

        self.logger = logger

        # Create Plugin Manager
        self.pluginManager = PluginManager(categories_filter={"Plugins": Plugin})
        self.pluginManager.setPluginPlaces(["plugins"])

    def isAdmin(self, user):
        for role in user.roles:
            if role.permissions.administrator:
                return True

        return False
 
    async def reloadPlugins(self):
        # Load Plugins
        self.pluginManager.locatePlugins()
        self.pluginManager.loadPlugins()

        # Uncomment to see full command registry logged  WARNING: There is a lot of text
        #logger.debug('Registry: %s', str(plugincommand.registry))

        # TODO: Make this a little more multi-server friendly
        disabledplugins = []
        settings = await self.getSettingsForTag(list(self.servers)[0], botcommands.BotCommands.TAG)

        if settings is not None and 'disabledplugins' in settings:
            disabledplugins = settings['disabledplugins'].split(',')

        if len(disabledplugins) == 1 and disabledplugins[0] is '':
            disabledplugins = []

        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            # Give the plugin it's dictionary of commands (so it doesn't need to lookup later)
            pluginCls = plugin.plugin_object.__class__.__name__
            if pluginCls in plugincommand.registry:
                plugin.plugin_object.parsedCommands = plugincommand.registry[pluginCls]
            else:
                plugin.plugin_object.parsedCommands = {}

            await plugin.plugin_object._init(plugin.name, self)
            logger.debug('%s Initialized!', plugin.name)

            for _, _disabledplugin in enumerate(disabledplugins):
                if plugin.plugin_object.tag == _disabledplugin or plugin.plugin_object.shortTag == _disabledplugin:
                    plugin.plugin_object.isDisabled = True
                    plugin.plugin_object.isDisabledPermanently = True

        self.commandCollisions = {}
        self.getCommandCollisions()

    def getCommandCollisions(self):
        # Generate a dictionary of tags & commands that collide
        for outer in self.pluginManager.getPluginsOfCategory("Plugins"):
            for inner in self.pluginManager.getPluginsOfCategory("Plugins"):
                if outer.name == inner.name:
                    continue

                # This should NEVER happen
                if outer.plugin_object.tag == inner.plugin_object.tag:
                    logger.error('Plugin Tag Collision! Tag: [%s]', outer.plugin_object.tag)

                # Check their commands to see if there is collision as well
                if outer.plugin_object.shortTag == inner.plugin_object.shortTag:
                    logger.warning('Plugin Short Tag Collision! Short Tag: [%s]', outer.plugin_object.shortTag)

                    for com in outer.plugin_object.parsedCommands:
                        if com in inner.plugin_object.parsedCommands:
                            logger.warning('Plugin Command Collision! Command: [%s]', com)

                            if outer.plugin_object.shortTag not in self.commandCollisions:
                                self.commandCollisions[outer.plugin_object.shortTag] = []

                            self.commandCollisions[outer.plugin_object.shortTag].append(com)

    async def shutdownPlugins(self):
        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            await plugin.plugin_object.shutdown()
            logger.debug('Shutdown %s', plugin.name)

        if self.voiceChannel != None:
            await self.voiceChannel.disconnect()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('-----------')
        logger.debug('Logged in as [%s] [%s]', self.user.name, self.user.id)

        botCmdCls = self.botCommands.__class__.__name__ 
        if botCmdCls in botcommand.registry:
            self.botCommands.parsedCommands = botcommand.registry[botCmdCls]
            await self.botCommands._init(bot=self)

        await self.reloadPlugins()
        print('Plugins initialized!')

    def isBotCommand(self, command):
        return self.botCommands.isCommand(command)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if not await self._executeBotCommand(message.content, message.server, message.channel, message.author):
            await self._readMessage(message)

            if not await self._checkForCommandCollisions(message.content, message.channel):
                await self._executePluginCommand(message.content, message.server, message.channel, message.author)

    def _parseTextForCommandInfo(self, text):
        results = {}

        # If we have a command, extract the command and parameters (if any)
        if text.startswith('!'):
            tmp = text.split(' ', 1)
            tmp[0] = tmp[0][1:] # get rid of !
            content = ''

            # Grab the rest of the string
            if len(tmp) > 1:
                content = tmp[1]

            results['tag'] = tmp[0]
            results['content'] = content

            tmp = content.split(' ', 1)
            results['command'] = tmp[0]

            if len(tmp) > 1:
                results['args'] = tmp[1]
            else:
                results['args'] = ''

            return results

        return None

    async def _executeBotCommand(self, text, _server, _channel, _author, **kwargs):
        commandInfo = self._parseTextForCommandInfo(text)

        if commandInfo is not None:
            tag = commandInfo['tag']
            content = commandInfo['content']

            # If we have a bot command, execute it
            if self.isBotCommand(tag):
                index, args = self.botCommands.parseCommandArgs(tag, content)

                if index == -1:
                    await self.send_message(_channel, 'Incorrect use of command `{}`. Please see the usage to learn how to properly use this command.\nJust Type: `!usage {}`'.format(tag, tag))
                    return True

                await self.botCommands.executeCommand(index, args, **kwargs, command=tag, server=_server, channel=_channel, author=_author)
                return True
            # This isn't a bot command and there was nothing after it. This must be an unrecognized command.
            elif content == '':
                await self.send_message(_channel, 'That is not a recognized command. For help, please try `!help`')
                return True

        # Otherwise, assume it is a plugin command
        return False

    async def _checkForCommandCollisions(self, text, channel):
        # Check for tag/command collisions here and resolve before letting the plugins handle it
        for key, array in self.commandCollisions.items():
            for value in array:
                if text.startswith('!' + key + ' ' + value):
                    logger.debug('There is more than one plugin with this short tag and command combination. Please use the full tag.')
                    await self.send_message(channel, 'There is more than one plugin with this short tag and command combination. Please use the full tag.')
                    return True

        return False

    async def _readMessage(self, message):
        # Go through each of the plugins and let them read the message
        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            if not plugin.plugin_object.isDisabled and plugin.plugin_object.isReadingMessages():
                await plugin.plugin_object.readMessage(message)

    async def _executePluginCommand(self, text, _server, _channel, _author, **kwargs):
        commandInfo = self._parseTextForCommandInfo(text)

        if commandInfo is not None:
            tag = commandInfo['tag']
            command = commandInfo['command']
            args = commandInfo['args']

            found = False
            # Go through each of the plugins and see if they can execute the command
            for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
                # Check if a plugin can handle the command and execute it if they can
                if tag != None and command != None and plugin.plugin_object.isCommand(tag, command):
                    if plugin.plugin_object.isDisabled:
                        found = True
                        await self.send_message(_channel, 'This plugin is currently disabled. To use commands, please enable it first.')
                        continue

                    index, temp = plugin.plugin_object.parseCommandArgs(command, args)
                    tag = plugin.plugin_object.tag # Update the tag for better feedback

                    if index == -1:
                        await self.send_message(_channel, 'Incorrect use of command `{}`. Please see the usage to learn how to properly use this command.\nJust type: `!usage {} {}`'.format(command, tag, command))
                        return

                    await plugin.plugin_object.executeCommand(index, temp, command=command, server=_server, channel=_channel, author=_author, **kwargs) 
                    found = True

            if not found and text.startswith('!'):
                await self.send_message(_channel, 'That is not a recognized command. For help, please try `!help`')

    def download_image(self, imgUrl, filename):
        try:
            logger.debug('[download_image]: Opening url')
            with urllib.request.urlopen(imgUrl) as imageOnWeb:
                logger.debug('[download_image]: Checking if url is image')
                if imageOnWeb.info()['Content-Type'].startswith('image'):
                    logger.debug('[download_image]: Reading Image')
                    buf = imageOnWeb.read()
                    logger.debug('[download_image]: Creating file [%s]', os.getcwd() + '/' + filename)
                    downloadedImage = open(os.getcwd() + '/' + filename, 'wb')
                    logger.debug('[download_image]: Writing Image')
                    downloadedImage.write(buf)
                    downloadedImage.close()
                    imageOnWeb.close()
                else:
                    logger.debug('[download_image]: Image URL is not an image')
                    return False
        except:
            logger.debug('[download_image]: Something failed while reading or writing the image')
            return False
        logger.debug('[download_image]: Successfully downloaded image')
        return True

    # Private helper for Settings API
    async def _createSettingsChannel(self, server):
        logger.debug('No settings found in server %s, creating settings.', server)
        return await self.create_channel(server, self.settingsChannelName)

    # Private helper for Settings API
    async def _getSettingsFromChannel(self, channel):
        # Create a dictionary from the settings and return it
        result = {}

        async for message in self.logs_from(channel, limit=1000000):
            if message.content.startswith('_'):
                temp = message.content.split('=', 1)[0][1:]
                tag = temp.split(':', 1)[0]
                key = temp.split(':', 1)[1]

                value = message.content.split('=', 1)[1]

                if tag not in result:
                    result[tag] = {}

                result[tag][key] = value

        return result

    # Private helper for Settings API
    async def _getSettingsFromChannelForTag(self, channel, plugintag):
        # Create a dictionary from the settings and return it
        result = {}

        async for message in self.logs_from(channel, limit=1000000):
            if message.content.startswith('_'):
                temp = message.content.split('=', 1)[0][1:]
                tag = temp.split(':', 1)[0]
                key = temp.split(':', 1)[1]

                if tag != plugintag:
                    continue

                value = message.content.split('=', 1)[1]

                result[key] = value

        return result

    # Private helper for Settings API
    async def _getMessageFromSettings(self, channel, tag, key):
        async for message in self.logs_from(channel, limit=1000000):
            if message.content.startswith('_' + tag + ':' + key):
                return message

        return None

    # Private helper for Settings API
    async def _getSettingsChannel(self, server):
        channel = discord.utils.get(server.channels, name=self.settingsChannelName, type=discord.ChannelType.text)

        if channel == None:
            channel = await self._createSettingsChannel(server)

        return channel

    # Private helper for Settings API
    async def _createSetting(self, channel, tag, key, value):
        logger.debug('Creating Setting [%s:%s] with value [%s]', tag, key, value)
        await self.send_message(channel, '_{}:{}={}'.format(str(tag), str(key), str(value)))

    # Private helper for Settings API
    async def _modifySetting(self, message, tag, key, value):
        logger.debug('Modifying Setting [%s:%s] with value [%s]', tag, key, value)
        await self.edit_message(message, '_{}:{}={}'.format(str(tag), str(key), str(value)))

    # Private helper for Settings API
    async def _deleteSetting(self, message):
        logger.debug('Deleting Setting')
        await self.delete_message(message)

    # Gets the settings object from the server
    # Settings object structure:
    # object[plugintag][settingname] = settingvalue
    async def getSettings(self, server):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)

            logger.debug('Settings constructed for server %s.', srv)
            return await self._getSettingsFromChannel(channel)

        logger.debug('The bot is not part of server %s!', server)
        return None

    # Gets the settings object from the server for a specific plugin tag
    # Settings object structure:
    # object[settingname] = settingvalue
    async def getSettingsForTag(self, server, tag):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)

            logger.debug('Settings constructed for server %s.', srv)
            return await self._getSettingsFromChannelForTag(channel, tag)

        logger.debug('The bot is not part of server %s!', server)
        return None

    # Modifies the setting if it exists and creates it if it doesn't
    async def modifySetting(self, server, tag, key, value):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)
            message = await self._getMessageFromSettings(channel, tag, key)

            if message == None:
                await self._createSetting(channel, tag, key, value)
            else:
                await self._modifySetting(message, tag, key, value)

            return

        logger.debug('The bot is not part of server %s!', server)

    # Deletes the setting
    async def deleteSetting(self, server, tag, key):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)
            message = await self._getMessageFromSettings(channel, tag, key)

            if message != None:
                await self._deleteSetting(message)

            return

        logger.debug('The bot is not part of server %s!', server)

    # Returns whether the server has a specific setting
    async def hasSetting(self, server, tag, key):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)
            message = await self._getMessageFromSettings(channel, tag, key)

            if message == None:
                return False
            else:
                return True

        logger.debug('The bot is not part of server %s!', server)
        return False

    # Returns the user's object if it exists. The username can be their discord name or server nickname
    def getUserFromName(self, server, username):
        user = None

        for member in server.members:
            if member.display_name == username:
                user = member
                break

        if not user:
            user = discord.utils.get(server.members, name=username)

        if not user:
            return None

        return user

if __name__ == "__main__":

    client = discord.Client()

    # Setup logging for the bot
    logger = logging.getLogger('styrobot')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='styrobot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))
    logger.addHandler(handler)

    styrobot = Bot()
    f = open('credentials.txt', 'r')
    creds = f.read().splitlines()
    email = creds[0]
    password = creds[1]
    f.close()
    #styrobot.run(email, password)
    styrobot.run(password)
