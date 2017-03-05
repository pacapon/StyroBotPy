import styrobot
import logging
import commands
import discord
import os
import glob
import shutil
import re
import random

class BotCommands:
    async def _init(self, bot):
        self.defaultParserType = commands.ParamParserType.SPACES
        self.defaultParser = commands.CommandRegistry.PARAM_PARSER_SPACES
        self.logger = logging.getLogger('styrobot.BotCommands')
        self.bot = bot

        # Uncomment to see full command registry for the bot commands  WARNING: There is a lot of text
        #self.logger.debug('Plugin Class: %s', self.__class__.__name__)
        #self.logger.debug('Commands: %s', str(self.parsedCommands))

    # Gets the list of commands and their descriptions that this bot can do
    # Format: !<commandname> <parameters>  - <description>
    # example: !save <url> <name>  - Saves the file at <url> to a local file named <name>
    # @return  An array of help strings
    def getCommandHelp(self):
        return commands.CommandHelper._getCommandHelp(self.parsedCommands)

    # Checks if the bot handles the command provided by the user
    # @param command  The command the user wants to execute
    # @return         Returns False if it can't handle it, True if it can
    def isCommand(self, command):
        return commands.CommandHelper._isCommand(self.parsedCommands, command)

    # Parses the args based on the command's settings
    # @param command  The command the user wants to execute
    # @param args     The remaining text, which will be parsed into args for execution
    # @return         Returns the parsed args in an array
    def parseCommandArgs(self, command, args):
        return commands.CommandHelper._parseCommandArgs(self.parsedCommands, command, args, self.defaultParser, self.defaultParserType, self.logger)
    
    # Executes the chat command
    # @param args       Any extra parameters that followed the command
    # @param kwargs     The information for the command
    async def executeCommand(self, index, args, **kwargs):
        await commands.CommandHelper._executeCommand(self, self.parsedCommands, index, args, self.logger, **kwargs)

    @styrobot.botcommand('Change the bot\'s avatar image. Url must be an PNG or JPG image.', name='changebotavatar', parserType=commands.ParamParserType.ALL)
    async def _changebotavatar_(self, channel, image_url, **kwargs):
        """
        Changes the bot's avatar to the image you provide. Only images with a .jpg or .png extension will work.
        `!changebotavatar <image_url>`
        **Example:** `!changebotavatar www.website.com/url_to_image.png`
        """

        extension = ''

        if '.jpg' in image_url.lower():
            extension = '.jpg'
        elif '.png' in image_url.lower():
            extension = '.png'
        else:
            self.logger.debug('[changebotavatar]: Url provided is either not an image or an unsupported format. Please make sure the image is a .png or .jpg')
            await self.bot.send_message(channel, 'Url provided is either not an image or an unsupported format. Please make sure the image is a .png or .jpg')
            return

        self.logger.debug('[changebotavatar]: Downloading image at url [%s]', image_url)

        if not self.bot.download_image(image_url, 'images/botavatar' + extension):
            self.logger.debug('[changebotavatar]: Failed to download image.')
            await self.bot.send_message(channel, 'Failed to download image.')
            return

        file = open('images/botavatar' + extension, 'rb')
        bytes = file.read()

        self.logger.debug('[changebotavatar]: Changing bot avatar.')

        if self.bot.user.bot:
            self.logger.debug('[changebotavatar]: User is a bot account.')
            await self.bot.edit_profile(None, avatar=bytes)
        else:
            await self.bot.edit_profile(password, avatar=bytes)

        self.logger.debug('[changebotavatar]: The Bot\'s Avatar has been updated.')
        await self.bot.send_message(channel, 'The Bot\'s Avatar has been updated.')

    @styrobot.botcommand('Change the name of the bot to <name>', name='changebotname', parserType=commands.ParamParserType.ALL)
    async def _changebotname_(self, server, name, **kwargs):
        """
        Changes the bot's server nickname to the name you provide. 
        `!changebotname <name>`
        **Example:** `!changebotname He-man, Master of the Universe`
        """

        await self.bot.change_nickname(server.me, name)

    @styrobot.botcommand('Clean image and music assets', name='cleanassets')
    async def _cleanassets_(self, channel, author, **kwargs):
        """
        Cleans the image and music assets cached by the bot.
        `!cleanassets`
        **Example:** `!cleanassets`
        """

        self.logger.debug('[cleanassets]: Cleaning assets.')
        if self.bot.isAdmin(author):
            # clean music files
            shutil.rmtree('music/')
            os.mkdir('music/')
            self.logger.debug('[cleanassets]: Cleaned music assets.')

            # clean image files
            for file in glob.glob('images/*'):
                if not file.endswith('f14.jpg'):
                    os.remove(file)

            self.logger.debug('[cleanassets]: Cleaned image assets.')

            await self.bot.send_message(channel, 'Cleaned music and image assets.')
            return

        self.logger.debug('[cleanassets]: %s, You do not have permission to do that.', author)
        await self.bot.send_message(channel, '<@' + author.id + '>, You do not have permission to do that.')

    @styrobot.botcommand('Create an F14!', name='f14')
    async def _f14_(self, channel, **kwargs):
        """
        Posts an image of an F14.
        `!f14`
        **Example:** `!f14`
        """

        await self.bot.send_file(channel, 'images/f14.jpg')

    @styrobot.botcommand('Help has never been so unhelpful', name='halp')
    async def _halp_(self, channel, **kwargs):
        """
        Scambles the help howto message.
        `!halp`
        **Example:** `!halp`
        """

        await self.getHelp(channel, '', True)

    @styrobot.botcommand('Help has never been so unhelpful', name='halp')
    async def _halpPage_(self, channel, page_name, **kwargs):
        """
        Scambles the help message for the bot or specific plugin.
        `!halp <page_name>`
        **Example for bot:** `!halp bot`
        **Example for plugin:** `!halp music`
        """

        await self.getHelp(channel, page_name, True)

    @styrobot.botcommand('Say Hello', name='hello')
    async def _hello_(self, channel, author, **kwargs):
        """
        Says hello!
        `!hello`
        **Example:** `!hello`
        """
        
        await self.bot.send_message(channel, 'Hello <@' + author.id + '>')

    @styrobot.botcommand('Provides the basic help page', name='help')
    async def _help_(self, channel, **kwargs):
        """
        Displays the basic howto message for the bot. This explains how to use commands.
        `!help`
        **Example:** `!help`
        """

        await self.getHelp(channel, '')

    @styrobot.botcommand('Provides the help page for a specific part of the bot or its plugins', name='help')
    async def _helpPage_(self, channel, page_name, **kwargs):
        """
        Displays the help for the bot or a specific plugin. This shows the different commands available.
        `!help <page_name>`
        **Example for bot:** `!help bot`
        **Example for plugin:** `!help music`
        """

        await self.getHelp(channel, page_name)

    @styrobot.botcommand('Join voice channel with given name', name='join')
    async def _join_(self, server, channel, author, name, **kwargs):
        """
        Tells the bot to join the voice channel with the given name. This is not case sensitive unless there are multiple channels with the same name. If there are multiple channels with the same name you will need to provide the exact, case sensitive, name.
        `!join <name>`
        **Example when not case sensitive:** `!join general`
        **Example when case sensitive:** `!join GeNerAl`
        """

        temp = []
        chan = None
        for channel in server.channels:
            if channel.type == discord.ChannelType.voice:
                if channel.name.lower() == name.lower():
                    temp.append(channel)

        if len(temp) == 0:
            self.logger.debug('[join]: Invalid channel name.')
            await self.bot.send_message(channel, 'Invalid channel name.')
            return
        elif len(temp) == 1:
            chan = temp[0]
        else:
            self.logger.debug('[join]: More than one channel with name found. Picking the channel with the same capitalization.')
            for channel in temp:
                if channel.name == name:
                    chan = channel
                    break

            if chan == None:
                self.logger.debug('[join]: There is more than one channel with this name. Please use the correct capitalization to join a specific one.')
                await self.bot.send_message(channel, 'There is more than one channel with this name. Please use the correct capitalization to join a specific one.')
                return

        await self._joinVoiceChannel(channel, author, chan, **kwargs)

    @styrobot.botcommand('Join voice channel you are currently in', name='join')
    async def _joinme_(self, server, channel, author, **kwargs):
        """
        Tells the bot to join the voice channel you are currently in.
        `!join`
        **Example:** `!join`
        """

        chan = author.voice.voice_channel

        if chan is None:
            self.logger.debug('[join]: You are not currently in a voice channel.')
            await self.bot.send_message(channel, 'You are not currently in a voice channel.')
            return

        await self._joinVoiceChannel(channel, author, chan, **kwargs)

    @styrobot.botcommand('Leave the current voice channel', name='leave')
    async def _leave_(self, channel, author, **kwargs):
        """
        Tells the bot to leave the voice channel it is currently in. Only the person who brought it into the voice channel (or an admin) can do this.
        `!leave`
        **Example:** `!leave`
        """

        if author == self.bot.voiceStarter or self.bot.isAdmin(author):
            for plugin in self.bot.pluginManager.getPluginsOfCategory("Plugins"):
                await plugin.plugin_object.onLeaveVoiceChannel()

            self.logger.debug('[leave]: Leaving voice channel %s', self.bot.voiceChannel.channel.name)
            await self.bot.voiceChannel.disconnect()
            self.bot.voiceChannel = None
            self.bot.voiceStarter = None
            return

        self.logger.debug('[leave]: You do not have permission to do that. You must be an admin or the person who did the join command.')
        await self.bot.send_message(channel, 'You do not have permission to do that. You must be an admin or the person who did the join command.')
        return

    @styrobot.botcommand('Reloads the plugins dynamically at runtime', name='reload')
    async def _reload_(self, channel, author, **kwargs):
        """
        Reloads the plugins the bot is using at runtime. This can only be done by an admin.
        `!reload`
        **Example:** `!reload`
        """

        if self.bot.isAdmin(author):
            await self.bot.reloadPlugins()
            return

        self.logger.debug('[reload]: %s, You do not have permission to do that.', author)
        await self.bot.send_message(channel, '<@' + author.id + '>, You do not have permission to do that.')

    @styrobot.botcommand('Shutdown the bot (requires server admin permissions)', name='shutdown')
    async def _shutdown_(self, channel, author, **kwargs):
        """
        Shuts down the bot. This can only be done by an admin.
        `!shutdown`
        **Example:** `!shutdown`
        """

        if self.bot.isAdmin(author):
            # Call shutdown on our plugins
            await self.bot.shutdownPlugins()

            await self.bot.logout()
            return

        self.logger.debug('[shutdown]: %s, You do not have permission to do that.', author)
        await self.bot.send_message(channel, '<@' + author.id + '>, You do not have permission to do that.')

    @styrobot.botcommand('Get the basic help page for the usage command', name='usage')
    async def _usage_(self, channel, **kwargs):
        """
        Provides documentation on usage:
        `!usage`
        """
        await self.getUsage(channel, None, None)

    @styrobot.botcommand('Shows the usage for a bot command', name='usage')
    async def _usageBot_(self, channel, botcommand, **kwargs):
        """
        Provides documentation on the bot command you specify:
        `!usage <botcommand>`
        **Example:** `!usage help`
        """
        await self.getUsage(channel, None, botcommand)

    @styrobot.botcommand('Shows the usage for a plugin command', name='usage')
    async def _usagePlugin_(self, channel, tag, command, **kwargs):
        """
        Provides documentation on the plugin command you specify:
        `!usage <plugin tag> <command>`
        **Example with plugin tag:** `!usage troll rickroll`
        **Example with plugin alias:** `!usage t rickroll`
        """
        await self.getUsage(channel, tag, command)

    def getUsageHowTo(self):
        helpStr = '__**How to use usage:**__\n'
        helpStr += 'Usage is a command designed to help you understand how to use commands. When you provide a command, it will display the command\'s structure and examples for how to use it.\n\n'

        return helpStr

    async def getUsage(self, channel, tag, command):
        if tag == None:
            if command == None:
                self.logger.debug('[usage]: Getting basic usage page.')

                await self.bot.send_message(channel, self.getUsageHowTo())

                await self.getUsage(channel, None, 'usage')
            else:
                if command in self.parsedCommands:
                    usageStr = '__**Usage for {}:**__\n'.format(command)
                    commandStr = ''
                    
                    for i, commandUsage in enumerate(self.parsedCommands[command][commands.CommandRegistry.USAGE]):
                        if commandUsage is not None:
                            if i is not 0: commandStr += '\n' 
                            commandStr += commandUsage + '\n'

                    if commandStr.replace('\n', '') == '':
                        self.logger.debug('[usage]: This command does not have any usage documentation.')
                        await self.bot.send_message(channel, 'This command does not have any usage documentation.')
                    else:
                        self.logger.debug('[usage]: Getting usage string for {}'.format(command))
                        await self.bot.send_message(channel, usageStr + commandStr)
                else:
                    self.logger.debug('[usage]: {} is not a valid bot command'.format(command))
                    await self.bot.send_message(channel, '{} is not a valid bot command'.format(command))
        else:
            self.logger.debug('[usage]: Plugin tag is: {}'.format(tag))

            found = False
            for _plugin in self.bot.pluginManager.getPluginsOfCategory("Plugins"):
                plugin = _plugin.plugin_object

                # Check if a plugin can handle the command and execute it if they can
                if plugin.isCommand(tag, command):
                    found = True
                    usageStr = '__**Usage for {}:**__\n'.format(command)
                    commandStr = ''

                    for i, commandUsage in enumerate(plugin.parsedCommands[command][commands.CommandRegistry.USAGE]):
                        if commandUsage is not None:
                            if i is not 0: commandStr += '\n' 
                            commandStr += commandUsage + '\n'

                    if commandStr.replace('\n', '') == '':
                        self.logger.debug('[usage]: This command does not have any usage documentation.')
                        await self.bot.send_message(channel, 'This command does not have any usage documentation.')
                    else:
                        self.logger.debug('[usage]: Getting usage string for {}'.format(command))
                        await self.bot.send_message(channel, usageStr + commandStr)

                    return

            if not found:
                self.logger.debug('[usage]: `{}` is not a valid command for plugin `{}`'.format(command, tag))
                await self.bot.send_message(channel, '`{}` is not a valid command for plugin `{}`'.format(command, tag))

    def getHelpBot(self):
        helpStr = '__**Basic Commands:**__\n'
        commands = self.getCommandHelp()

        for com in commands:
            helpStr += com + '\n'

        self.logger.debug('[help]: Getting bot help page.')

        return helpStr

    def getHelpHowTo(self):
        helpStr = '__**How to use commands:**__\n'
        helpStr += 'The command structure is like this: `!<tag> <command> <arguments>`\n\n'
        helpStr += 'You must always start with an `!` and this is immediately followed with a `tag`. Each plugin has its own specific tag which you have to use to execute one of its commands. These tags are *unique* and no two plugins will have the same one.\n\n'
        helpStr += 'Since these tags can get long and tedious, each plugin also has an `alias`. You can use this instead of the tag to reduce typing. If two plugins have the same alias, you will have to use the tag.\n\n'
        helpStr += 'Plugins might also have commands. This is what follows the tag, separated with a space. See the help page for a Plugin to know what commands it has.\n\n'
        helpStr += 'Some commands don\'t require any additional arguments, to learn more about this how commands are used, type `!usage`\n\n'
        helpStr += 'The bot also has special commands which follow a slightly different command structure than plugins. They are just `!<command>`. These are unique to the bot itself and a plugin will never do this.\n\n'
        helpStr += '**Example plugin command 1:** `!music play`\n'
        helpStr += '**Example plugin command 2:** `!m queue throughthefireandflames`\n'
        helpStr += '**Example bot command:** `!hello`\n\n'
        helpStr += '__**More help:**__\n'
        helpStr += 'To see which commands the bot has, type `!help bot`\n'
        helpStr += 'To see which plugins the bot has, type `!help plugins` or `!help tags`\n'
        helpStr += 'To see which commands a plugin has, type `!help <tag>` or `!help <alias>`\n'
        helpStr += 'To see all commands available for the bot and all plugins, type `!help all`\n\n'
        return helpStr

    def getHelpPluginTags(self):
        helpStr = '__**Plugin Tags:**__\n\n'
        helpStr += 'Use `!help <plugintag>` or `!help <pluginalias>` to see which commands a plugin has.\n'
        helpStr += 'To see which commands the bot has, type `!help bot`\n'
        helpStr += 'To see all commands available, type `!help all`\n\n'

        for plugin in self.bot.pluginManager.getPluginsOfCategory("Plugins"):
            helpStr += '**[' + plugin.name + ']** Tag: **' + plugin.plugin_object.tag + '**  Alias: **' + plugin.plugin_object.shortTag + '**\n'

        return helpStr

    async def getHelp(self, channel, command, scrambleMessage = False):
        async def send_message(bot, channel, message, scrambleMessage):
            if scrambleMessage:
                await bot.send_message(channel, BotCommands._scramble(message))
            else:
                await bot.send_message(channel, message)

        if command == '':
            self.logger.debug('[help]: Getting basic help page.')

            await send_message(self.bot, channel, self.getHelpHowTo(), scrambleMessage)

        elif command == 'all':
            self.logger.debug('[help]: Getting all help pages.')
            
            await send_message(self.bot, channel, self.getHelpBot(), scrambleMessage)

            for plugin in self.bot.pluginManager.getPluginsOfCategory("Plugins"):
                pluginHelp = ''
                commands = plugin.plugin_object.getCommandHelp()

                pluginHelp += '\n__**' + plugin.name + ' Commands:**__\n'
                pluginHelp += '**Tag:** ' + plugin.plugin_object.tag + '\n'
                pluginHelp += '**Alias:** ' + plugin.plugin_object.shortTag + '\n'
                pluginHelp += '**Usage:** `!usage {} <command>` or `!usage {} <command>`\n\n'.format(plugin.plugin_object.tag, plugin.plugin_object.shortTag)

                for com in commands:
                    if len(pluginHelp) + len(com + '\n') < 2000:
                        pluginHelp += com + '\n'
                    else:
                        await send_message(self.bot, channel, pluginHelp, scrambleMessage)
                        pluginHelp = '';

                if pluginHelp:
                    await send_message(self.bot, channel, pluginHelp, scrambleMessage)

        elif command == 'bot':
            self.logger.debug('[help]: Getting bot help page.')
            await send_message(self.bot, channel, self.getHelpBot(), scrambleMessage)

        elif command == 'plugin' or command == 'plugins' or command == 'tags':
            self.logger.debug('[help]: Getting bot help page.')
            await send_message(self.bot, channel, self.getHelpPluginTags(), scrambleMessage)

        else:
            self.logger.debug('[help]: Finding plugin with tag/shortTag [%s]', command)
            # Check for short tag collision
            if command in self.bot.commandCollisions:
                self.logger.debug('There is more than one plugin with this short tag. Please use the full tag.')
                await self.bot.send_message(channel, 'There is more than one plugin with this alias. Please use the tag.')
                return 

            # See if the command is the tag or short tag for a plugin
            for plugin in self.bot.pluginManager.getPluginsOfCategory("Plugins"):
                if command == plugin.plugin_object.tag or command == plugin.plugin_object.shortTag:
                    pluginHelp = ''
                    commands = plugin.plugin_object.getCommandHelp()

                    pluginHelp += '\n__**' + plugin.name + ' Commands:**__\n'
                    pluginHelp += '**Tag:** ' + plugin.plugin_object.tag + '\n'
                    pluginHelp += '**Alias:** ' + plugin.plugin_object.shortTag + '\n'
                    pluginHelp += '**Usage:** `!usage {} <command>` or `!usage {} <command>`\n\n'.format(plugin.plugin_object.tag, plugin.plugin_object.shortTag)

                    for com in commands:
                        if len(pluginHelp) + len(com + '\n') < 2000:
                            pluginHelp += com + '\n'
                        else:
                            await send_message(self.bot, channel, pluginHelp, scrambleMessage)
                            pluginHelp = '';

                    if pluginHelp:
                        await send_message(self.bot, channel, pluginHelp, scrambleMessage)

                    self.logger.debug('[help]: Plugin found; getting help page.')

    def _scramble(sentence):
        words = sentence.split()

        for i in range(len(words)):
            m = re.search('([`_*~]+)(.+)([`_*~]+)', words[i])

            if m:
                prefix = m.group(1)
                content = m.group(2)
                suffix = m.group(3)

                content = list(content)
                random.shuffle(content)
                content = ''.join(content)
                words[i] = prefix + content + suffix

            else:
                words[i] = list(words[i])
                random.shuffle(words[i])
                words[i] = ''.join(words[i])

        return ' '.join(words)

    async def _joinVoiceChannel(self, channel, author, chan, **kwargs):
        # Leave the current channel before joining (throws exception otherwise)
        if self.bot.voiceChannel is not None:
            await self._leave_(channel, author, **kwargs)

        self.logger.debug('[join]: Joining channel %s', chan)
        self.bot.voiceChannel = await self.bot.join_voice_channel(chan)
        self.bot.voiceStarter = author

        for plugin in self.bot.pluginManager.getPluginsOfCategory("Plugins"):
            await plugin.plugin_object.onJoinVoiceChannel()

