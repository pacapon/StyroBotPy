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
    PARAM_PARSER = 'paramParser'
    PARAM_PARSER_TYPE = 'paramParserType'
    PARAM_PARSER_SPACES = lambda args: args.split(' ')
    PARAM_PARSER_ALL = lambda args: args

    def __init__(self):
        self.registry = {}

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

            if 'parser' in kwargs:
                commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER] = kwargs['parser']
                commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE] = ParamParserType.CUSTOM
            else:
                if 'parserType' in kwargs:
                    isValid = lambda enumVal: True if enumVal in ParamParserType and enumVal != ParamParserType.CUSTOM else False

                    if isValid(kwargs['parserType']):
                        commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE] = kwargs['parserType']
                        commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER] = getattr(CommandRegistry, 'PARAM_PARSER_' + kwargs['parserType'].name)
                    else:
                        commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE] = ParamParserType.SPACES
                        commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER] = CommandRegistry.PARAM_PARSER_SPACES
                else:
                    commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE] = ParamParserType.SPACES
                    commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER] = CommandRegistry.PARAM_PARSER_SPACES


            #print('Registry Parser:', commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER])
            #print('Registry Parser Type:', commandRegistry.registry[className][commandName][CommandRegistry.PARAM_PARSER_TYPE])

            return func
        return decorator

    commandRegistrar.registry = commandRegistry.registry
    return commandRegistrar

commandRegistry = CommandRegistry()

