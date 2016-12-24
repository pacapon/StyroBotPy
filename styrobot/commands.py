import inspect
import enum

class ParamParserType(enum.Enum):
    SPACES = 'SPACES'
    ALL = 'ALL'
    CUSTOM = 'CUSTOM'

class CommandRegistry():
    # Command dictionary keys
    NUM_PARAMS = 'numParams'
    PARAM_NAMES = 'paramNames'
    DESCRIPTION = 'description'
    COMMAND_NAME = 'name'
    FUNCTION_NAME = 'funcName'
    OVERRIDE_DEFAULT_PARSER = 'overrideDefaultParser'
    PARAM_PARSER = 'paramParser'
    PARAM_PARSER_TYPE = 'paramParserType'
    PARAM_PARSER_SPACES = lambda args: args.split(' ')
    PARAM_PARSER_ALL = lambda args: args

    def __init__(self):
        self.registry = {}

class BaseCommandStructure:
    # Gets the help information for the commands provided in a nicely formatted string
    # Format 1 (bot commands):    !<commandname> <parameters>  - <description>
    # Format 2 (plugin commands): !<tag> <commandname> <parameters>  - <description>
    # example 1: !file save <url> <name>  - Saves the file at <url> to a local file named <name>
    # example 2: !hello  - Say Hello
    # @param commandList    The list of commands 
    # @param tag            The plugin's tag (optional)
    # @return  An array of help strings
    def _getCommandHelp(commandList, tag = None):
        commands = []

        for key, value in commandList.items():
            if tag is not None:
                str = '`!{} {} '.format(tag, key)
            else:
                str = '`!{} '.format(key)
        
            if len(value[CommandRegistry.PARAM_NAMES]) != 0:
                for paramName in value[CommandRegistry.PARAM_NAMES]:
                    str += '<{}> '.format(paramName)

            str += '`  - {}'.format(value[CommandRegistry.DESCRIPTION])
            commands.append(str)

        return commands

    # Checks if the command provided by the user is handled and returns the parsed arguments if it does
    # @param commandList        The list of commands 
    # @param command            The command the user wants to execute
    # @param args               The remaining text, which will be parsed into args for execution
    # @param defaultParser      The default parser to use on the args if an override isn't given
    # @param defaultParserType  The type of the default parser
    # @param logger             The logger to use (not required)
    # @return                   Returns False if it can't handle it. If it can, it returns the parsed args in an array
    def _checkForCommand(commandList, command, args, defaultParser, defaultParserType, logger = None):
        for key, value in commandList.items():
            if key == command:
                num = int(value[CommandRegistry.NUM_PARAMS])
                temp = defaultParser(args)
                parserType = defaultParserType 
                
                if value[CommandRegistry.OVERRIDE_DEFAULT_PARSER] == True:
                    temp = value[CommandRegistry.PARAM_PARSER](args)
                    parserType = value[CommandRegistry.PARAM_PARSER_TYPE]

                if logger is not None:
                    logger.debug('Command Found!')
                    logger.debug('ParserType: %s', parserType)

                # Break out early if no params
                if num == 0:
                    if logger is not None: logger.debug('Args: []')
                    return []

                # Break out early if we want all the arguments as a parameter
                if parserType == ParamParserType.ALL:
                    if logger is not None: logger.debug('Args: [%s]', temp)
                    return [temp]

                if logger is not None: logger.debug('Args: %s', temp[:num])
                return temp[:num]

        return False

    # Executes the command
    # @param obj            The object that has the function for the command being called
    # @param commandList    The list of commands
    # @param args           Any extra parameters that followed the command
    # @param logger         The logger to use (not required)
    # @param kwargs         The information for the command
    async def _executeCommand(obj, commandList, args, logger = None, **kwargs):
        command = kwargs.pop('command')
        num = commandList[command][CommandRegistry.NUM_PARAMS]
        paramNames = commandList[command][CommandRegistry.PARAM_NAMES]
        funcName = commandList[command][CommandRegistry.FUNCTION_NAME]

        if len(args) != len(paramNames):
            if logger is not None: logger.error('The number of arguments (%s) and the number of parameter names (%s) does not match!', len(args), len(paramNames))

        for i, name in enumerate(paramNames):
            kwargs[name] = args[i]

        if logger is not None: logger.debug('Executing command [%s] with arguments [%s]', command, str(args)[1:-1])
        await getattr(obj, funcName)(**kwargs)


# Reference for auto registering decorated functions for a class
# http://stackoverflow.com/questions/3054372/auto-register-class-methods-using-decorator
# I should explore this and see if I can use it

# Reference for auto registering decorated functions
# http://stackoverflow.com/questions/5707589/calling-functions-by-array-index-in-python/5707605#5707605

def _loadCommands():
    def commandRegistrar(description, **kwargs):
        def decorator(func):
            className = func.__qualname__.split('.', 1)[0]
            funcName = func.__name__
            commandName = kwargs[CommandRegistry.COMMAND_NAME] if CommandRegistry.COMMAND_NAME in kwargs else funcName
            params = []

            for i, key in enumerate(inspect.signature(func).parameters):
                # remove things that are not important
                if key is not 'self' and key is not 'server' and \
                   key is not 'channel' and key is not 'author' and \
                   key is not 'kwargs':
                    params.append(key)

            #print('Class Name:', className)
            #print('Command Name:', commandName)
            #print('Func Name:', funcName)
            #print('Params:', params)
            #if 'parser' in kwargs: print('Parser:', kwargs['parser'])
            #if 'parserType' in kwargs: print('Parser Type:', kwargs['parserType'])

            if className not in commandRegistry.registry:
                commandRegistry.registry[className] = {}

            if commandName not in commandRegistry.registry[className]:
                commandRegistry.registry[className][commandName] = {}

            commandRegistry.registry[className][commandName][CommandRegistry.FUNCTION_NAME] = funcName
            commandRegistry.registry[className][commandName][CommandRegistry.NUM_PARAMS] = len(params) 
            commandRegistry.registry[className][commandName][CommandRegistry.PARAM_NAMES] = params 
            commandRegistry.registry[className][commandName][CommandRegistry.DESCRIPTION] = description 
            commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE] = ParamParserType.SPACES
            commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER] = CommandRegistry.PARAM_PARSER_SPACES
            commandRegistry.registry[className][commandName][CommandRegistry.OVERRIDE_DEFAULT_PARSER] = False

            if 'parser' in kwargs:
                commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER] = kwargs['parser']
                commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE] = ParamParserType.CUSTOM
                commandRegistry.registry[className][commandName][CommandRegistry.OVERRIDE_DEFAULT_PARSER] = True
            elif 'parserType' in kwargs:
                isValid = lambda enumVal: True if enumVal in ParamParserType and enumVal != ParamParserType.CUSTOM else False

                if isValid(kwargs['parserType']):
                    commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE] = kwargs['parserType']
                    commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER] = getattr(CommandRegistry, 'PARAM_PARSER_' + kwargs['parserType'].name)
                    commandRegistry.registry[className][commandName][CommandRegistry.OVERRIDE_DEFAULT_PARSER] = True

            #print('Registry Parser:', commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER])
            #print('Registry Parser Type:', commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE])

            return func
        return decorator

    commandRegistrar.registry = commandRegistry.registry
    return commandRegistrar

commandRegistry = CommandRegistry()

