from plugin import Plugin

class HighRoller(Plugin):
    
    async def initialize(self, bot):
        self.bot = bot
        self.commands = []
        
    def getCommands(self):
        commands = []

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                print('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters):
        pass

    def shutdown(self):
        print('Shutdown HighRoller')
