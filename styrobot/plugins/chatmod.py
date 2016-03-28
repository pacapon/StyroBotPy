from plugin import Plugin

class ChatMod(Plugin):

    def initialize(self, bot):
        self.bot = bot
        self.bannedWords = []
        self.commands = []

        self.commands.append('!showbanned')
        self.commands.append('!banword')
        self.commands.append('!unbanword')

        for server in self.bot.servers:
            channel = discord.utils.get(server.channels, name='ChatModSettings', type=ChannelType.text)

            if channel == None:
                channel = self.bot.create_channel(server, 'ChatModSettings')

            # do something with channel

        try:
            f = open('chatmodsettings.txt', 'r+')
            contents = f.read().splitlines()
            
            for line in contents:
                if line.startswith('='):
                    self.bannedWords.append(line[1:])

        except IOError:
            f = open('chatmodsettings.txt', 'w')
            f.write('=poop')
            f.close()

    def getCommands(self):
        commands = []

        commands.append('!showbanned   - Shows the list of banned words')
        commands.append('!banword <word>   - Adds <word> to the list of banned words')
        commands.append('!unbanword <word>   - Removes <word> from the list of banned words')

        return commands;

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                print('Command Found!')
                return True

        return False

    async def executeCommand(self, channel, command, parameters):
        print('Executing command: ' + command + ' with parameters: ' + parameters + ' on channel: ' + channel.name)

        if command == '!showbanned':
            if len(self.bannedWords) > 0:
                words = ''
                for word in self.bannedWords:
                    words += word + '\n'

                print(words)
                await self.bot.send_message(channel, words)
            else:
                await self.bot.send_message(channel, 'There are currently no banned words.')
        elif command == '!banword' and parameters != '':
            # TODO: check to see if word is already there before banning
            # TODO: save banned word to list stored in private chat

            firstWord = parameters.split(' ', 1)[0]

            self.bannedWords.append(firstWord)
            print('Banning word: ' + firstWord)
        elif command == '!unbanword' and parameters != '':
            # TODO: remove word from banned list
            # TODO: remove word from list stored in private chat
            print('Unbanning word: ' + parameters)

    def isReadingMessages(self):
        return True

    async def readMessage(self, message):
        print('Reading message!')
        for word in self.bannedWords:
            if word in message.content:
                # TODO: give better warning when banned word used
                # TODO: do something to user when they use a banned word too much
                await self.bot.send_message(message.channel, 'Banned word used')
                print('Banned word used')

    def shutdown(self):
        print('Shutdown ChatMod')
