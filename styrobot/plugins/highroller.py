from plugin import Plugin
import random

class HighRoller(Plugin):
    
    async def initialize(self, bot):
        self.bot = bot
        self.commands = []

        self.commands.append('!roll')
        self.commands.append('!flipcoin')
        
    def getCommands(self):
        commands = []

        commands.append('**!roll <number>**   - Rolls a dice of size <number>')
        commands.append('**!flipcoin**   - Flips a coin')

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                print('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters):
        if command == '!roll' and parameters != '':
           firstWord = parameters.split(' ', 1)[0]

           if self.isNumber(firstWord) and int(firstWord) > 0:
               result = self.rollDice(int(firstWord))

               print(author.name + ' rolled a ' + str(result))
               await self.bot.send_message(channel, author.name + ' rolled a ' + str(result))

        elif command == '!flipcoin':
            result = self.rollDice(2)

            if result == 1:
                print('Heads!')
                await self.bot.send_message(channel, 'Heads!')
            else:
                print('Tails!')
                await self.bot.send_message(channel, 'Tails!')

    def rollDice(self, num):
        return random.randint(1, num)

    def isNumber(self, num):
        try:
            int(num)
            return True
        except ValueError:
            return False
