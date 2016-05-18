#!/usr/bin/env python
import discord
from yapsy.PluginManager import PluginManager
from plugin import Plugin

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

client = discord.Client()

class Bot(discord.Client):
    def __init__(self):
        super().__init__()

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
            print(plugin.name + ' Initialized!')

    async def shutdownPlugins(self):
        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            await plugin.plugin_object.shutdown()
            print('Shutdown ' + plugin.name)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('-----------')

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
                if role.permissions.manage_roles: # Change manage_roles if you want a different permission level to be able to do this

                    # Call shutdown on our plugins
                    await self.shutdownPlugins()

                    await self.logout()
                    break
            return 
        elif message.content.startswith('!hello'):
            await self.send_message(message.channel, 'Hello World!')
            return
        elif message.content.startswith('!f14'):
            await self.send_file(message.channel, 'images/f14.jpg')
            return
        elif message.content.startswith('!changebotname'):
            newName = message.content[14:].strip()
            await self.edit_profile(password, username=newName)
            return
        elif message.content.startswith('!reload'):
            print('Reloading plugins!')
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
               
  
if __name__ == "__main__":
    styroBot = Bot()
    f = open('credentials.txt', 'r')
    creds = f.read().splitlines()
    email = creds[0]
    password = creds[1]
    f.close()
    #styroBot.run(email, password)
    styroBot.run(password)
