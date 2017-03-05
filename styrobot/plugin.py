import abc
import logging
import inspect
from commands import CommandRegistry, ParamParserType, CommandHelper 

class Plugin:
    __metaclass__ = abc.ABCMeta

    # Private initialize function
    # DO NOT OVERRIDE OR CALL EXPLICITELY
    async def _init(self, name, bot):
        self.bot = bot
        self.tag = name
        self.shortTag = name[0]
        self.defaultParserType = ParamParserType.SPACES
        self.defaultParser = CommandRegistry.PARAM_PARSER_SPACES
        self.logger = logging.getLogger('styrobot.' + name)

        await self.initialize(bot)
        
        # Uncomment to see full command registry for this plugin  WARNING: There is a lot of text
        #self.logger.debug('Plugin Class: %s', self.__class__.__name__)
        #self.logger.debug('Commands: %s', str(self.parsedCommands))

    # Initializes the plugin
    # @param bot  A reference to the bot's instance
    @abc.abstractmethod
    async def initialize(self, bot): pass

    # Gets the list of commands and their descriptions that this plugin can do
    # Format: !<tag> <commandname> <parameters>  - <description>
    # example: !file save <url> <name>  - Saves the file at <url> to a local file named <name>
    # @return  An array of help strings
    def getCommandHelp(self):
        return CommandHelper._getCommandHelp(self.parsedCommands, self.tag)

    # Checks if this plugin handles the command provided by the user
    # @param tag      The tag which identifies the plugin (this could be their short tag)
    # @param command  The command the user wants to execute
    # @param args     The remaining text, which will be parsed into args for execution
    # @return         Returns False if it can't handle it. If it can, it returns the parsed args in an array
    def isCommand(self, tag, command):
        if tag != self.tag and tag != self.shortTag:
            return False

        return CommandHelper._isCommand(self.parsedCommands, command)

    def parseCommandArgs(self, command, args):
        return CommandHelper._parseCommandArgs(self.parsedCommands, command, args, self.defaultParser, self.defaultParserType, self.logger)

    
    # Executes the chat command
    # @param args       Any extra parameters that followed the command
    # @param kwargs     The information for the command
    async def executeCommand(self, index, args, **kwargs):
        await CommandHelper._executeCommand(self, self.parsedCommands, index, args, self.logger, **kwargs)

    # Whether or not this plugin wants to read messages completely
    # Override this if you want your plugin to read messages completely for something
    # @return  False if you don't want to read messages, True otherwise
    def isReadingMessages(self):
        return False

    # Allows the plugin to read the full message and do whatever they want with it
    # It is not recommend to handle commands in this function.
    # @param message  The message as given by discord. See discord documentation on the message class
    async def readMessage(self, message): pass

    # An event that is called when the bot joins a voice channel. Override if you need
    # to handle something when this happens
    async def onJoinVoiceChannel(self): pass

    # An event that is called when the bot leaves a voice channel. Override if you need
    # to handle something when this happens
    async def onLeaveVoiceChannel(self): pass

    # Shutdowns the plugin
    async def shutdown(self): pass

