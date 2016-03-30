from plugin import Plugin
import cleverbot

class CleverBotChat(Plugin):
    async def initialize(self, bot):
        self.cb = cleverbot.Cleverbot()
        self.bot = bot
        self.commands = []
        
        self.commands.append('!chat')

    def getCommands(self):
        commands = []
        
        commands.append('**!chat <message>**  - Sends a message to CleverBot')

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                print('Command Found!')
                return True

        return False

    async def executeCommand(self, channel, command, parameters):
        if command == '!chat' and parameters != '':
            response = self.cb.ask(parameters)
            await self.bot.send_message(channel, response)

    def shutdown(self):
        print('Shutdown CleverBotChat')
