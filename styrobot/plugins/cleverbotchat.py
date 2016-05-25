from plugin import Plugin
import cleverbot
import logging

class CleverBotChat(Plugin):
    async def initialize(self, bot):
        self.cb = cleverbot.Cleverbot()
        self.bot = bot
        self.commands = []
        self.logger = logging.getLogger('styrobot.cleverbotchat')
        
        self.commands.append('!chat')

    def getCommands(self):
        commands = []
        
        commands.append('**!chat <message>**  - Sends a message to CleverBot')

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                self.logger.debug('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters):
        if command == '!chat' and parameters != '':
            self.logger.debug('[!chat] [%s]: %s', author, parameters)
            response = self.cb.ask(parameters)
            self.logger.debug('[!chat] [cleverbot]: %s', response)
            await self.bot.send_message(channel, response)
