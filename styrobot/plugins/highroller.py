from plugin import Plugin
import random
import logging

class HighRoller(Plugin):
    
    async def initialize(self, bot):
        self.bot = bot
        self.commands = []
        self.callFlip = {}
        self.logger = logging.getLogger('styrobot.highroller')

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
                self.logger.debug('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters):
        if command == '!roll' and parameters != '':
           firstWord = parameters.split(' ', 1)[0]

           if self.isNumber(firstWord) and int(firstWord) > 0:
               result = self.rollDice(int(firstWord))

               self.logger.debug('[!roll]: %s rolled a %s', author, str(result))
               await self.bot.send_message(channel, '<@' + author.id + '> rolled a ' + str(result))
           else:
               self.logger.debug('[!roll]: You can\'t roll a dice smaller than 1.')
               await self.bot.send_message(channel, 'You can\'t roll a dice smaller than 1.')

        elif command == '!callflip' and parameters != '':
            firstWord = parameters.split(' ', 1)[0]
            firstWord = firstWord.lower()

            if firstWord == 'head' or firstWord == 'heads':
                self.callFlip[str(author)] = ['heads', author.id]
            elif firstWord == 'tail' or firstWord == 'tails':
                self.callFlip[str(author)] = ['tails', author.id]

            if len(self.callFlip) == 2:
                p1name = ''
                p1call = ''
                p1id = ''
                message = ''
                logmessage = ''
                result = self.flipCoin().lower()
                for key, value in self.callFlip.items():
                    if p1name == '' and p1call == '':
                        p1name = key
                        p1call = value[0]
                        p1id = value[1]
                    else:
                        if result == p1call and result == value[0]:
                            message = 'It is a tie between <@' + p1id + '> and <@' + value[1] + '>!'
                            logmessage = 'It is a tie between ' + p1name + ' and ' + key + '!'
                        elif result == p1call and result != value[0]:
                            message = '<@' + p1id + '> wins the coin flip!' 
                            logmessage = p1name + ' wins the coin flip!' 
                        elif result == value[0] and result != p1call:
                            message = '<@' + value[1] + '> wins the coin flip!' 
                            logmessage = key + ' wins the coin flip!' 
                        else:
                            message = 'Nobody wins the coin flip!'
                            
                        break

                self.callFlip = {}
                self.logger.debug('[!callflip]: %s', logmessage)
                await self.bot.send_message(channel, message)

        elif command == '!flipcoin':
            result = self.flipCoin()
            self.logger.debug('[!flipcoin]: %s!', result)
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
