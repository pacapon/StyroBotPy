from plugin import Plugin
import discord
import re

class ChatMod(Plugin):

    async def initialize(self, bot):
        self.bot = bot
        self.bannedWords = []
        self.commands = []
        self.userWarnings = {}
        self.maxWarnings = 2 # How many warnings should a user get before action is taken

        # What action to take on a user after they've maxed out their warnings
        # Options are: kick and ban
        self.banAction = 'kick' 

        self.commands.append('!showbanned')
        self.commands.append('!cmsettings')
        self.commands.append('!cmmaxwarn')
        self.commands.append('!cmbanact')
        self.commands.append('!cmstatus')
        self.commands.append('!banword')
        self.commands.append('!unbanword')

        print('This Bot is part of ' + str(len(self.bot.servers)) + ' servers!')

        for server in self.bot.servers:
            self.channel = discord.utils.get(server.channels, name='chatmodsettings', type=discord.ChannelType.text)

            if self.channel == None:
                print('No settings found, creating channel')
                self.channel = await self.bot.create_channel(server, 'chatmodsettings')

                await self.bot.send_message(self.channel, '_maxwarn=' + self.maxWarnings)
                await self.bot.send_message(self.channel, '_banact=', + self.banAction)

            else:
                print('Settings found, loading channel info')

                async for message in self.bot.logs_from(self.channel, limit=1000000):
                    if message.content.startswith('='):
                        self.bannedWords.append(message.content[1:])
                    elif message.content.startswith('_maxwarn='):
                        self.maxWarnings = message.content[9:]
                    elif message.content.startswith('_banact='):
                        self.banAction = message.content[8:]

    def getCommands(self):
        commands = []

        commands.append('**!showbanned**   - Shows the list of banned words')
        commands.append('**!cmsettings**   - Show the current settings for the chat mod plugin')
        commands.append('**!cmmaxwarn <number>**   - Set the max number of warnings to <number>')
        commands.append('**!cmbanact <action>**   - Change the action to take when a player has hit their max warnings (kick, ban)')
        commands.append('**!cmstatus**   - Check your current warning status')
        commands.append('**!banword <word>**   - Adds <word> to the list of banned words')
        commands.append('**!unbanword <word>**   - Removes <word> from the list of banned words')

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                print('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters):
        if command == '!showbanned':
            if len(self.bannedWords) > 0:
                words = ''
                for word in self.bannedWords:
                    words += word + '\n'

                print(words)
                await self.bot.send_message(channel, words)
            else:
                await self.bot.send_message(channel, 'There are currently no banned words.')
                print('There are currently no banned words.')

        elif command == '!cmsettings':
            print('Max Warnings: ' + str(self.maxWarnings) + '\nBan Action: ' + self.banAction)
            await self.bot.send_message(channel, 'Max Warnings: ' + str(self.maxWarnings) + '\nBan Action: ' + self.banAction)

        elif command == '!cmmaxwarn' and parameters != '':
            if int(parameters) < 0:
                print('You cant have negative max warnings.')
                await self.bot.send_message(channel, 'You cant have negative max warnings.')
            else:
                firstWord = parameters.split(' ', 1)[0]

                self.maxWarnings = int(firstWord)
                await self.updateMessage('_maxwarn=', '_maxwarn=' + str(firstWord))

                print('Max Warnings have been set to: ' + str(firstWord))
                await self.bot.send_message(channel, 'Max Warnings have been set to: ' + str(firstWord))

        elif command == '!cmbanact' and parameters != '':
            firstWord = parameters.split(' ', 1)[0]

            if firstWord == 'kick' or firstWord == 'ban':
                self.banAction = firstWord
                await self.updateMessage('_banact=', '_banact=' + firstWord)

                print('Ban Action has been set to: ' + firstWord)
                await self.bot.send_message(channel, 'Ban Action has been set to: ' + firstWord)
            else:
                print('Invalid Ban Action. Please use kick or ban')
                await self.bot.send_message(channel, 'Invalid Ban Action. Please use kick or ban')

        elif command == '!cmstatus':
            if author.name in self.userWarnings:
                print(author.name + ', you have ' + str(self.userWarnings[author.name]) + ' warnings.')
                await self.bot.send_message(channel, author.name + ', you have ' + str(self.userWarnings[author.name]) + ' warnings.')

            else:
                print(author.name + ', you have been given no warnings yet.')
                await self.bot.send_message(channel, author.name + ', you have been given no warnings yet.')

        elif command == '!banword' and parameters != '':
            firstWord = parameters.split(' ', 1)[0]
            firstWord = self.scrubMessage(firstWord)

            if not firstWord in self.bannedWords:
                self.bannedWords.append(firstWord)
                await self.bot.send_message(self.channel, '=' + firstWord)

                print('Banning word: ' + firstWord)
                await self.bot.send_message(channel, 'Banning word: ' + firstWord)
                
        elif command == '!unbanword' and parameters != '':
            firstWord = parameters.split(' ', 1)[0]
            firstWord = self.scrubMessage(firstWord)

            if firstWord in self.bannedWords:
                self.bannedWords.remove(firstWord)
                await self.removeMessage(firstWord)

                print('Unbanning word: ' + firstWord)
                await self.bot.send_message(channel, 'Unbanning word: ' + firstWord)

            else:
                print('This word is not banned.')
                await self.bot.send_message(channel, 'This word is not banned.')

    async def removeMessage(self, word):
        async for message in self.bot.logs_from(self.channel, limit=1000000):
            if message.content.startswith('='):
                if message.content[1:] == word:
                    await self.bot.delete_message(message)
                    return

    async def updateMessage(self, start, newMessage):
        async for message in self.bot.logs_from(self.channel, limit=1000000):
            if message.content.startswith(start):
                await self.bot.edit_message(message, newMessage)

    def isReadingMessages(self):
        return True

    async def readMessage(self, message):
        print('Reading message!')
        scrubbed = self.scrubMessage(message.content)

        for word in self.bannedWords:
            if word in scrubbed: 

                # TODO: improve this so people can't just bypass the moderating
                if message.content.startswith('!'):
                    return

                if message.author.name in self.userWarnings:
                    self.userWarnings[message.author.name] += 1

                    if self.userWarnings[message.author.name] > int(self.maxWarnings):
                        await self.applyAction(message.author, message.channel)
                        
                    elif self.userWarnings[message.author.name] == int(self.maxWarnings):
                        await self.bot.send_message(message.channel, 'Watch your language, ' + message.author.name + '. This is your final warning.')
                        print(message.author.name + ' has used the banned word: ' + word)
                    else:
                        await self.bot.send_message(message.channel, 'Watch your language, ' + message.author.name + '. You have been warned.')
                        print(message.author.name + ' has used the banned word: ' + word)

                else:
                    self.userWarnings[message.author.name] = 1

                    await self.bot.send_message(message.channel, 'Watch your language, ' + message.author.name + '. You have been warned.')
                    print(message.author.name + ' has used the banned word: ' + word)

    # Takes in the message's content and removes all markdown so it doesn't
    # screw up the detection as much
    def scrubMessage(self, message):
        scrubbedMessage = re.findall('[^_*\-\'\"\`\~]', message)
        print(''.join(scrubbedMessage).lower())

        return ''.join(scrubbedMessage).lower()

    async def applyAction(self, user, channel):
        if self.banAction == 'kick':
            print('Kicking ' + user.name + ' for bad language.') 
            await self.bot.send_message(channel, 'Kicking ' + user.name + ' for bad language.') 

            await self.bot.kick(user)

        elif self.banAction == 'ban':
            print('Banning ' + user.name + ' for bad language.')
            await self.bot.send_message(channel, 'Banning ' + user.name + ' for bad language.') 

            await self.bot.ban(user)

    def shutdown(self):
        print('Shutdown ChatMod')
