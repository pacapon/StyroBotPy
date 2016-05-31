import abc

class Plugin:
    __metaclass__ = abc.ABCMeta

    # Private initialize function
    # DO NOT OVERRIDE OR CALL EXPLICITELY
    async def _init(self, name, bot): 
        self.tag = name
        self.shortTag = name[0]
        self.commands = []

        await self.initialize(bot)
        
        self.parsedCommands = self._parseCommands()

    # Initializes the plugin
    # @param bot  A reference to the bot's instance
    @abc.abstractmethod
    async def initialize(self, bot): pass

    # Gets the list of commands and their descriptions that this plugin can do
    # Format: !<tag> <commandname> <parameters>  - <description>
    # example: !file save <url> <name>  - Saves the file at <url> to a local file named <name>
    # @return  An array of strings formatted like the example above
    def getCommands(self):
        commands = []

        for key, value in self.parsedCommands.items():
            str = '**!{} {} '.format(self.tag, key)
        
            if len(value['paramNames']) != 0:
                for paramName in value['paramNames']:
                    str += '<{}> '.format(paramName)

            str += '**  - {}'.format(value['description'])

            commands.append(str)

        return commands

    def _parseCommands(self):
        commands = {}
        for com in self.commands:
            temp = com.split('<')
            temp2 = temp[2].split('>')
            name = temp[1][:-1]
            description = temp[3][:-1]
            numParams = temp2[0]
            paramNames = []
            if (len(temp2) > 1 and ((numParams != '*' and int(numParams) != 0) or numParams == '*')):
                paramNames = temp2[1][1:-1].split(',')

            commands[name] = {}
            commands[name]['numParams'] = numParams
            commands[name]['paramNames'] = paramNames
            commands[name]['description'] = description

            print('Name: ', name)
            print('NumParams: ', numParams)
            print('ParamNames: ', paramNames)
            print('Description: ', description)

        return commands

    # Checks if this plugin handles the command provided by the user 
    # @return  True if you can handle this command, False otherwise 
    @abc.abstractmethod
    def checkForCommand(self, command): pass

    # Executes the chat command 
    # @param channel     The discord channel this command was executed in
    # @param author      The user which executed this command
    # @param command     The command to execute
    # @param args        Any extra parameters that followed the command
    async def executeCommand(self, server, channel, author, command, *args):
        await getattr(self, '_' + command + '_')(server, channel, author, *args)

    # Whether or not this plugin wants to read messages completely
    # Override this if you want your plugin to read messages completely for something
    # @return  False if you don't want to read messages, True otherwise
    def isReadingMessages(self):
        return False

    # Allows the plugin to read the full message and do whatever they want with it
    # It is not recommend to handle commands in this function.
    # @param message  The message as given by discord. See discord documentation on the message class 
    async def readMessage(self, message): pass

    # Shutdowns the plugin
    async def shutdown(self): pass
