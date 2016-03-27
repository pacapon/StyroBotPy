from plugin import Plugin

class ChatMod(Plugin):

    def initialize(self):
        self.bannedWords = []
        self.commands = []

        self.commands.append('!showbanned')
        self.commands.append('!banword')
        self.commands.append('!unbanword')

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

        print(self.bannedWords)

    def getCommands(self):
        commands = []

        commands.append('!showbanned   - Shows the list of banned words')
        commands.append('!banword <word>   - Adds <word> to the list of banned words')
        commands.append('!unbanword <word>   - Removes <word> from the list of banned words')

        return commands;

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                return True

        return False

    def executeCommand(self, command, parameters):
        if command == '!showbanned':
            print(self.bannedWords)
        elif command == '!banword' and parameters != '':
            print('Banning word: ' + parameters)
        elif command == '!unbanword' and parameters != '':
            print('Unbanning word: ' + parameters)

    def isReadingMessages(self):
        return True

    def readMessage(self, message):
        pass

    def shutdown(self):
        print('Shutdown ChatMod')
