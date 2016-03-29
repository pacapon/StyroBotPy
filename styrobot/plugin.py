import abc

class Plugin:
    __metaclass__ = abc.ABCMeta

    # Initializes the plugin
    # @param bot  A reference to the bot's instance
    async def initialize(self, bot): pass

    # Gets the list of commands and their descriptions that this plugin can do
    # Format: !<commandname> <parameters>  - <description>
    # example: !savefile <url> <name>  - Saves the file at <url> to a local file named <name>
    # @return  An array of strings formatted like the example above
    @abc.abstractmethod
    def getCommands(self): pass

    # Checks if this plugin handles the command provided by the user 
    # @return  True if you can handle this command, False otherwise 
    @abc.abstractmethod
    def checkForCommand(self, command): pass

    # Executes the chat command 
    # @param command     The command to execute
    # @param parameters  Any extra parameters that followed the command
    @abc.abstractmethod
    async def executeCommand(self, channel, command, parameters): pass

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
    def shutdown(self): pass
