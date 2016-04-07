from plugin import Plugin
import random

class HighRoller(Plugin):
    
    async def initialize(self, bot):
        self.bot = bot
        self.commands = []
        self.callFlip = {}

        self.commands.append('!roll')
        self.commands.append('!callflip')
        self.commands.append('!flipcoin')
        
    def getCommands(self):
        commands = []

        commands.append('**!roll <number>**   - Rolls a dice of size <number>')
        commands.append('**!callflip <name>**   - Call the next coinflip')
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

        elif command == '!callflip' and parameters != '':
            firstWord = parameters.split(' ', 1)[0]
            firstWord = firstWord.lower()

            if firstWord == 'head' or firstWord == 'heads':
                self.callFlip[author.name] = 'heads'
            elif firstWord == 'tail' or firstWord == 'tails':
                self.callFlip[author.name] = 'tails'

            if len(self.callFlip) == 2:
                p1name = ''
                p1call = ''
                message = ''
                result = self.flipCoin().lower()
                for key, value in self.callFlip.items():
                    if p1name == '' and p1call == '':
                        p1name = key
                        p1call = value
                    else:
                        if result == p1call and result == value:
                            message = 'It is a tie between ' + p1name + ' and ' + key + '!'
                        elif result == p1call and result != value:
                            message = p1call + ' wins the coin flip!' 
                        elif result == value and result != p1call:
                            message = key + ' wins the coin flip!' 
                        else:
                            message = 'Nobody wins the coin flip!'
                            
                        break

                self.callFlip = {}
                print(message)
                await self.bot.send_message(channel, message)

        elif command == '!flipcoin':
            result = self.flipCoin()
            print(result + '!')
            await self.bot.send_message(channel, result + '!'); 

    def rollDice(self, num):
        return random.randint(1, num)

    def flipCoin(self):
        result = self.rollDice(2)

        if result == 1:
            return 'Heads'
        else:
            return 'Tails'

    def isNumber(self, num):
        try:
            int(num)
            return True
        except ValueError:
            return False
