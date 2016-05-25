#!/usr/bin/env python
import discord
from yapsy.PluginManager import PluginManager
from plugin import Plugin
import logging

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

client = discord.Client()

class Bot(discord.Client):
    def __init__(self):
        super().__init__()

        self.settingsChannelName = 'botsettings' # change this if you want your bot settings channel to have a different name

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
        
    def getHelp(self):
        helpStr = '__**Basic Commands:**__\n'
        helpStr += '**!hello**   - Say Hello\n'
        helpStr += '**!f14**   - Create an F14!\n'
        helpStr += '**!changebotname <name>**   - Change the name of the bot to <name>\n'
        helpStr += '**!shutdown**   - Shutdown the bot (requires server admin permissions)\n'
        helpStr += '**!reload**   - Reloads the plugins dynamically at runtime\n'

        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            commands = plugin.plugin_object.getCommands()

            helpStr += '\n__**' + plugin.name + ' Commands:**__\n'

            for com in commands:
                helpStr += com + '\n'

        return helpStr

    async def reloadPlugins(self):
        # Load Plugins
        self.pluginManager.locatePlugins()
        self.pluginManager.loadPlugins()

        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            await plugin.plugin_object.initialize(self)
            logger.debug('%s Initialized!', plugin.name)

    async def shutdownPlugins(self):
        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            await plugin.plugin_object.shutdown()
            logger.debug('Shutdown %s', plugin.name)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('-----------')
        logger.debug('Logged in as [%s] [%s]', self.user.name, self.user.id)

        await self.reloadPlugins()

    async def on_message(self, message):
        if message.author == self.user:
            return

        # We do something special with basic built-in commands 
        # because we don't want plugins using these
        if (message.content.startswith('!help')):
            await self.send_message(message.channel, self.getHelp())
            return
        elif message.content.startswith('!shutdown'):
            for role in message.author.roles:
                if role.permissions.administrator: # Change administrator if you want a different permission level to be able to do this

                    # Call shutdown on our plugins
                    await self.shutdownPlugins()

                    await self.logout()
                    return 

            logger.debug('%s, You do not have permission to do that.', message.author)
            await self.send_message(message.channel, '<@' + message.author.id + '>, You do not have permission to do that.')
            return 
        elif message.content.startswith('!hello'):
            await self.send_message(message.channel, 'Hello <@' + message.author.id + '>')
            return
        elif message.content.startswith('!f14'):
            await self.send_file(message.channel, 'images/f14.jpg')
            return
        elif message.content.startswith('!changebotname'):
            newName = message.content[14:].strip()
            await self.edit_profile(password, username=newName)
            return
        elif message.content.startswith('!reload'):
            logger.debug('Reloading plugins!')
            await self.reloadPlugins()
            return

        command = ''
        parameters = ''
            
        # If we have a command, extract the command and parameters (if any)
        if message.content.startswith('!'):
            content =  message.content.split(' ', 1) 
            command = content[0]

            if len(content) > 1:
                parameters = content[1]

        # Go through each of the plugins and see if they can execute the command
        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            # Let the plugin read the message
            if plugin.plugin_object.isReadingMessages():
                await plugin.plugin_object.readMessage(message)

            # Check if a plugin can handle the command and execute it if they can
            if command != '' and plugin.plugin_object.checkForCommand(command):
                await plugin.plugin_object.executeCommand(message.server, message.channel, message.author, command, parameters)

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
                key = message.content.split('=', 1)[0][1:]
                value = message.content.split('=', 1)[1]

                result[key] = value

        return result

    # Private helper for Settings API
    async def _getMessageFromSettings(self, channel, key):
        async for message in self.logs_from(channel, limit=1000000):
            if message.content.startswith('_' + key):
                return message

        return None
 
    # Private helper for Settings API
    async def _getSettingsChannel(self, server):
        channel = discord.utils.get(server.channels, name=self.settingsChannelName, type=discord.ChannelType.text)

        if channel == None:
            channel = await self._createSettingsChannel(server)

        return channel

    # Private helper for Settings API
    async def _createSetting(self, channel, key, value):
        logger.debug('Creating Setting [%s] with value [%s]', key, value)
        await self.send_message(channel, '_{}={}'.format(str(key), str(value)))

    # Private helper for Settings API
    async def _modifySetting(self, message, key, value):
        logger.debug('Modifying Setting [%s] with value [%s]', key, value)
        await self.edit_message(message, '_{}={}'.format(str(key), str(value)))

    # Private helper for Settings API
    async def _deleteSetting(self, message):
        logger.debug('Deleting Setting')
        await self.delete_message(message)

    # Gets the settings object (a dictionary where the key is the setting's name and the value is the value) from the server
    async def getSettings(self, server):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)

            logger.debug('Settings constructed for server %s.', srv)
            return await self._getSettingsFromChannel(channel) 

        logger.debug('The bot is not part of server %s!', server)
        return None

    # Modifies the setting if it exists and creates it if it doesn't
    async def modifySetting(self, server, key, value):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)
            message = await self._getMessageFromSettings(channel, key)

            if message == None:
                await self._createSetting(channel, key, value)
            else:
                await self._modifySetting(message, key, value)

            return

        logger.debug('The bot is not part of server %s!', server)

    # Deletes the setting
    async def deleteSetting(self, server, key):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)
            message = await self._getMessageFromSettings(channel, key)

            if message != None:
                await self._deleteSetting(message)

            return

        logger.debug('The bot is not part of server %s!', server)

    # Returns whether the server has a specific setting
    async def hasSetting(self, server, key):
        for srv in self.servers:
            if srv != server:
                continue

            channel = await self._getSettingsChannel(srv)
            message = await self._getMessageFromSettings(channel, key)

            if message == None:
                return False
            else:
                return True

        logger.debug('The bot is not part of server %s!', server)
        return False

  
if __name__ == "__main__":

    # Setup logging for the bot
    logger = logging.getLogger('styrobot')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='styrobot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))
    logger.addHandler(handler)

    styroBot = Bot()
    f = open('credentials.txt', 'r')
    creds = f.read().splitlines()
    email = creds[0]
    password = creds[1]
    f.close()
    #styroBot.run(email, password)
    styroBot.run(password)
