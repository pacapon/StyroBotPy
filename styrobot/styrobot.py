#!/usr/bin/env python
import discord
from yapsy.PluginManager import PluginManager
from random import shuffle
from plugin import Plugin
import os
import glob
import shutil
import logging
import urllib.request
import inspect
import commands
import re

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

# Reference for auto registering decorated functions for a class
# http://stackoverflow.com/questions/3054372/auto-register-class-methods-using-decorator
# I should explore this and see if I can use it

# Reference for auto registering decorated functions
# http://stackoverflow.com/questions/5707589/calling-functions-by-array-index-in-python/5707605#5707605

# Plugin Command dictionary and decorator
plugincommand = commands._loadCommands()

class Bot(discord.Client):

    def __init__(self):
        super().__init__()

        self.settingsChannelName = 'botsettings' # change this if you want your bot settings channel to have a different name
        self.voiceChannel = None
        self.voiceStarter = None

        self.botCommands = []
        self.botCommands.append('help')
        self.botCommands.append('halp')
        self.botCommands.append('shutdown')
        self.botCommands.append('hello')
        self.botCommands.append('f14')
        self.botCommands.append('changebotname')
        self.botCommands.append('changebotavatar')
        self.botCommands.append('cleanassets')
        self.botCommands.append('join')
        self.botCommands.append('leave')
        self.botCommands.append('reload')

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

    def getHelpBot(self):
        helpStr = '__**Basic Commands:**__\n\n'
        helpStr += '`!hello`   - Say Hello\n'
        helpStr += '`!f14`   - Create an F14!\n'
        helpStr += '`!halp`   - Help has never been so unhelpful\n'
        helpStr += '`!changebotname <name>`   - Change the name of the bot to <name>\n'
        helpStr += '`!changebotavatar <image_url>`   - Change the bot\'s avatar image. Url must be an PNG or JPG image.\n'
        helpStr += '`!cleanassets`    - Clean image and music assets.\n'
        helpStr += '`!join <name>`   - Join voice channel with given name\n'
        helpStr += '`!leave`   - Leave the current voice channel\n'
        helpStr += '`!shutdown`   - Shutdown the bot (requires server admin permissions)\n'
        helpStr += '`!reload`   - Reloads the plugins dynamically at runtime\n'
        return helpStr

    def getHelpHowTo(self):
        helpStr = '__**How to use commands:**__\n'
        helpStr += 'The command structure is like this: `!<tag> <command> <arguments>`\n\n'
        helpStr += 'You must always start with an **!** and this is immediately followed with a **tag**. Each plugin has its own specific tag which you have to use to execute one of its commands.\n\n'
        helpStr += 'Since these tags can get long and tedious, each plugin also has a **short tag**. You can use this instead of the full tag to reduce typing. If two plugins have the same short tag, you will have to use the full tag.\n\n'
        helpStr += 'Plugins might also have commands. This is what follows the tag, separated with a space. See the help page for a Plugin to know what commands it has.\n\n'
        helpStr += 'Some commands don\'t require any additional arguments, but others do. Add these as shown by the help page for a Plugin.\n\n'
        helpStr += 'The bot also has special commands which don\'t follow the command structure. They are just `!<command>`. These are unique to the bot itself and a plugin will never do this.\n\n'
        helpStr += '**Example command 1:** `!music play`\n'
        helpStr += '**Example command 2:** `!m queue throughthefireandflames`\n'
        helpStr += '**Example command 3:** `!hello`'
        return helpStr

    def getHelpPluginTags(self):
        helpStr = '__**Plugin Tags:**__\n\n'
        helpStr += 'Use `!help <plugintag>` or `!help <pluginshorttag>` to see which commands a plugin has.\n'
        helpStr += 'To see which commands the bot has, type `!help bot`\n'
        helpStr += 'To see all commands available, type `!help all`\n\n'

        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            helpStr += '**[' + plugin.name + ']** Tag: **' + plugin.plugin_object.tag + '**  Short Tag: **' + plugin.plugin_object.shortTag + '**\n'

        return helpStr

    async def getHelp(self, channel, command):
        if command == '':
            logger.debug('[help]: Getting basic help page.')
            await self.send_message(channel, self.getHelpHowTo())

            await self.send_message(channel, self.getHelpBot())

            await self.send_message(channel, self.getHelpPluginTags())

        elif command == 'all':
            logger.debug('[help]: Getting all help pages.')
            await self.send_message(channel, self.getHelpBot())

            for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
                helpStr = ''
                commands = plugin.plugin_object.getCommands()

                helpStr += '\n__**' + plugin.name + ' Commands:**__\n'
                helpStr += '**Tag:** ' + plugin.plugin_object.tag + '\n'
                helpStr += '**ShortTag:** ' + plugin.plugin_object.shortTag + '\n'

                for com in commands:
                    if len(helpStr) + len(com + '\n') < 2000:
                        helpStr += com + '\n'
                    else:
                        await self.send_message(channel, helpStr)
                        helpStr = '';

                if helpStr:
                    await self.send_message(channel, helpStr)

        elif command == 'bot':
            logger.debug('[help]: Getting bot help page.')
            await self.send_message(channel, self.getHelpBot())

        else:
            logger.debug('[help]: Finding plugin with tag/shortTag [%s]', command)
            # Check for short tag collision
            if command in self.commandCollisions:
                logger.debug('There is more than one plugin with this short tag. Please use the full tag.')
                await self.send_message(channel, 'There is more than one plugin with this short tag. Please use the full tag.')
                return

            # See if the command is the tag or short tag for a plugin
            for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
                if command == plugin.plugin_object.tag or command == plugin.plugin_object.shortTag:
                    helpStr = ''
                    commands = plugin.plugin_object.getCommands()

                    helpStr += '\n__**' + plugin.name + ' Commands:**__\n'
                    helpStr += '**Tag:** ' + plugin.plugin_object.tag + '\n'
                    helpStr += '**ShortTag:** ' + plugin.plugin_object.shortTag + '\n'

                    for com in commands:
                        if len(helpStr) + len(com + '\n') < 2000:
                            helpStr += com + '\n'
                        else:
                            await self.send_message(channel, helpStr)
                            helpStr = '';

                    if helpStr:
                        await self.send_message(channel, helpStr)

                    logger.debug('[help]: Plugin found; getting help page.')
                    return

    def _scramble(self, sentence):
        words = sentence.split()

        for i in range(len(words)):
            m = re.search('([`_*~]+)(.+)([`_*~]+)', words[i])

            if m:
                prefix = m.group(1)
                content = m.group(2)
                suffix = m.group(3)

                content = list(content)
                shuffle(content)
                content = ''.join(content)
                words[i] = prefix + content + suffix

            else:
                words[i] = list(words[i])
                shuffle(words[i])
                words[i] = ''.join(words[i])

        return ' '.join(words)

    async def getHalp(self, channel, command):
        if command == '':
            logger.debug('[halp]: Getting basic halp page.')
            await self.send_message(channel, self._scramble(self.getHelpHowTo()))

            await self.send_message(channel, self._scramble(self.getHelpBot()))

            await self.send_message(channel, self._scramble(self.getHelpPluginTags()))

        elif command == 'all':
            logger.debug('[halp]: Getting all halp pages.')
            await self.send_message(channel, self._scramble(self.getHelpBot()))

            for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
                helpStr = ''
                commands = plugin.plugin_object.getCommands()

                helpStr += '\n__**' + plugin.name + ' Commands:**__\n'
                helpStr += '**Tag:** ' + plugin.plugin_object.tag + '\n'
                helpStr += '**ShortTag:** ' + plugin.plugin_object.shortTag + '\n'

                for com in commands:
                    if len(helpStr) + len(com + '\n') < 2000:
                        helpStr += com + '\n'
                    else:
                        await self.send_message(channel, self._scramble(helpStr))
                        helpStr = '';

                if helpStr:
                    await self.send_message(channel, self._scramble(helpStr))

        elif command == 'bot':
            logger.debug('[halp]: Getting bot halp page.')
            await self.send_message(channel, self._scramble(self.getHelpBot()))

        else:
            logger.debug('[halp]: Finding plugin with tag/shortTag [%s]', command)
            # Check for short tag collision
            # Check for short tag collision
            if command in self.commandCollisions:
                logger.debug('There is more than one plugin with this short tag. Please use the full tag.')
                await self.send_message(channel, 'There is more than one plugin with this short tag. Please use the full tag.')
                return

            # See if the command is the tag or short tag for a plugin
            for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
                if command == plugin.plugin_object.tag or command == plugin.plugin_object.shortTag:
                    helpStr = ''
                    commands = plugin.plugin_object.getCommands()

                    helpStr += '\n__**' + plugin.name + ' Commands:**__\n'
                    helpStr += '**Tag:** ' + plugin.plugin_object.tag + '\n'
                    helpStr += '**ShortTag:** ' + plugin.plugin_object.shortTag + '\n'

                    for com in commands:
                        if len(helpStr) + len(com + '\n') < 2000:
                            helpStr += com + '\n'
                        else:
                            await self.send_message(channel, self._scramble(helpStr))
                            helpStr = '';

                    if helpStr:
                        await self.send_message(channel, self._scramble(helpStr))

                    logger.debug('[halp]: Plugin found; getting halp page.')
                    return

    async def reloadPlugins(self):
        # Load Plugins
        self.pluginManager.locatePlugins()
        self.pluginManager.loadPlugins()

        logger.debug('Registry: %s', str(plugincommand.registry))

        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            # Give the plugin it's dictionary of commands (so it doesn't need to lookup later)
            if plugin.plugin_object.__class__.__name__ in plugincommand.registry:
                plugin.plugin_object.parsedCommands = plugincommand.registry[plugin.plugin_object.__class__.__name__]
            else:
                plugin.plugin_object.parsedCommands = {}

            await plugin.plugin_object._init(plugin.name, self)
            logger.debug('%s Initialized!', plugin.name)

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

        await self.reloadPlugins()
        print('Plugins initialized!')

    def isBotCommand(self, tag):
        if tag in self.botCommands:
            return True

        return False

    async def on_message(self, message):
        if message.author == self.user:
            return

        tag = ''
        command = ''
        args = ''

        # If we have a command, extract the command and parameters (if any)
        if message.content.startswith('!'):
            content =  message.content.split(' ', 2)
            tag = content[0][1:]

            if len(content) > 1:
                command = content[1]
            elif not self.isBotCommand(tag):
                await self.send_message(message.channel, 'That is not a recognized command. For help, please try !help')
                return

            if len(content) > 2:
                args = content[2]

        # We do something special with basic built-in commands
        # because we don't want plugins using these
        if tag == 'help':
            await self.getHelp(message.channel, command)
            return
        elif tag == 'halp':
            await self.getHalp(message.channel, command)
            return
        elif tag == 'shutdown':
            logger.debug('[shutdown]: Executing command shutdown.')
            if self.isAdmin(message.author):
                # Call shutdown on our plugins
                await self.shutdownPlugins()

                await self.logout()
                return

            logger.debug('[shutdown]: %s, You do not have permission to do that.', message.author)
            await self.send_message(message.channel, '<@' + message.author.id + '>, You do not have permission to do that.')
            return
        elif tag =='hello':
            logger.debug('[hello]: Executing command hello.')
            await self.send_message(message.channel, 'Hello <@' + message.author.id + '>')
            return
        elif tag == 'f14':
            logger.debug('[f14]: Executing command f14.')
            await self.send_file(message.channel, 'images/f14.jpg')
            return
        elif tag == 'changebotname':
            newName = message.content[14:].strip()
            logger.debug('[changebotname]: Executing command changebotname with args [%s].', newName)

            await self.change_nickname(message.server.me, newName)
            return
        elif tag == 'changebotavatar':
            avatarUrl = message.content[17:]
            extension = ''

            if '.jpg' in avatarUrl.lower():
                extension = '.jpg'
            elif '.png' in avatarUrl.lower():
                extension = '.png'
            else:
                logger.debug('[changebotavatar]: Url provided is either not an image or an unsupported format. Please make sure the image is a .png or .jpg')
                await self.send_message(message.channel, 'Url provided is either not an image or an unsupported format. Please make sure the image is a .png or .jpg')
                return

            logger.debug('[changebotavatar]: Downloading image at url [%s]', avatarUrl)

            if not self.download_image(avatarUrl, 'images/botavatar' + extension):
                logger.debug('[changebotavatar]: Failed to download image.')
                await self.send_message(message.channel, 'Failed to download image.')
                return

            file = open('images/botavatar' + extension, 'rb')
            bytes = file.read()

            logger.debug('[changebotavatar]: Changing bot avatar.')

            if self.user.bot:
                logger.debug('[changebotavatar]: User is a bot account.')
                await self.edit_profile(None, avatar=bytes)
            else:
                await self.edit_profile(password, avatar=bytes)

            logger.debug('[changebotavatar]: The Bot\'s Avatar has been updated.')
            await self.send_message(message.channel, 'The Bot\'s Avatar has been updated.')
            return
        elif tag == 'cleanassets':
            logger.debug('[cleanassets]: Cleaning assets.')
            if self.isAdmin(message.author):
                # clean music files
                shutil.rmtree('music/')
                os.mkdir('music/')
                logger.debug('[cleanassets]: Cleaned music assets.')

                # clean image files
                for file in glob.glob('images/*'):
                    if not file.endswith('f14.jpg'):
                        os.remove(file)

                logger.debug('[cleanassets]: Cleaned image assets.')

                await self.send_message(message.channel, 'Cleaned music and image assets.')
                return

            logger.debug('[cleanassets]: %s, You do not have permission to do that.', message.author)
            await self.send_message(message.channel, '<@' + message.author.id + '>, You do not have permission to do that.')
            return
        elif tag == 'join':
            temp = []
            chan = None
            for channel in message.server.channels:
                if channel.type == discord.ChannelType.voice:
                    if channel.name.lower() == command.lower():
                        temp.append(channel)

            if len(temp) == 0:
                self.logger.debug('[join]: Invalid channel name.')
                await self.send_message(message.channel, 'Invalid channel name.')
                return
            elif len(temp) == 1:
                chan = temp[0]
            else:
                self.logger.debug('[join]: More than one channel with name found. Picking the channel with the same capitalization.')
                for channel in temp:
                    if channel.name == command:
                        chan = channel
                        break

                if chan == None:
                    self.logger.debug('[join]: There is more than one channel with this name. Please use the correct capitalization to join a specific one.')
                    await self.send_message(message.channel, 'There is more than one channel with this name. Please use the correct capitalization to join a specific one.')
                    return


            self.logger.debug('[join]: Joining channel %s', chan)
            self.voiceChannel = await self.join_voice_channel(chan)
            self.voiceStarter = message.author

            for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
                await plugin.plugin_object.onJoinVoiceChannel()
            return
        elif tag == 'leave':
            if message.author == self.voiceStarter or self.isAdmin(message.author):
                for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
                    await plugin.plugin_object.onLeaveVoiceChannel()

                self.logger.debug('[leave]: Leaving voice channel %s', self.voiceChannel.channel.name)
                await self.voiceChannel.disconnect()
                self.voiceChannel = None
                self.voiceStarter = None
                return

            self.logger.debug('[leave]: You do not have permission to do that. You must be an admin or the person who did the join command.')
            await self.send_message(message.channel, 'You do not have permission to do that. You must be an admin or the person who did the join command.')
            return
        elif tag == 'reload':
            if self.isAdmin(message.author):
                logger.debug('[reload]: Executing command reload')
                await self.reloadPlugins()
                return

            logger.debug('[shutdown]: %s, You do not have permission to do that.', message.author)
            await self.send_message(message.channel, '<@' + message.author.id + '>, You do not have permission to do that.')
            return

        # Check for tag/command collisions here and resolve before letting the plugins handle it
        for key, array in self.commandCollisions.items():
            for value in array:
                if message.content.startswith('!' + key + ' ' + value):
                    logger.debug('There is more than one plugin with this short tag and command combination. Please use the full tag.')
                    await self.send_message(message.channel, 'There is more than one plugin with this short tag and command combination. Please use the full tag.')
                    return

        found = False
        # Go through each of the plugins and see if they can execute the command
        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            # Let the plugin read the message
            if plugin.plugin_object.isReadingMessages():
                await plugin.plugin_object.readMessage(message)

            # Check if a plugin can handle the command and execute it if they can
            if tag != '' and command != '':
                temp = plugin.plugin_object.checkForCommand(tag, command, args)

                if temp != False:
                    await plugin.plugin_object.executeCommand(temp, command=command, server=message.server, channel=message.channel, author=message.author) 
                    found = True

        if not found and message.content.startswith('!'):
            await self.send_message(message.channel, 'That is not a recognized command. For help, please try !help')

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
