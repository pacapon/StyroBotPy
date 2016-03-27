from plugin import Plugin
#import cleverbot

class CleverBotChat(Plugin):
    def initialize(self):
        #self.cb = cleverbot.Cleverbot()
        print('CleverBotChat Initialized!')

    def getCommands(self):
        commands = []
        
        commands.append('!chat <message>  - Sends a message to CleverBot')

        return commands

    def checkForCommand(self, command):
        print ('Checking for command: ' + command)
        return True

    def executeCommand(self, command, parameters):
        print('Executing command: ' + command + ' with parameters: ' + parameters)

    def isReadingMessages(self):
        return True

    def readMessage(self, message):
        print(message.author.name + ' sent message: ' + message.content)

    def shutdown(self):
        print('Shutdown CleverBotChat')
