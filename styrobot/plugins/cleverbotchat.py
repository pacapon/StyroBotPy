from plugin import Plugin
#import cleverbot

class CleverBotChat(Plugin):
    def initialize(self, bot):
        #self.cb = cleverbot.Cleverbot()
        pass

    def getCommands(self):
        commands = []
        
        commands.append('!chat <message>  - Sends a message to CleverBot')

        return commands

    def checkForCommand(self, command):
        #print ('Checking for command: ' + command)
        return True

    async def executeCommand(self, channel, command, parameters):
        #print('Executing command: ' + command + ' with parameters: ' + parameters + ' on channel: ' + channel.name)
        pass

    def isReadingMessages(self):
        return True

    async def readMessage(self, message):
        print(message.author.name + ' sent message: ' + message.content)

    def shutdown(self):
        print('Shutdown CleverBotChat')
