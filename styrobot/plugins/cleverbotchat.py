from plugin import Plugin
import cleverbot
import logging
import styrobot
import commands

class CleverBotChat(Plugin):
    async def initialize(self, bot):
        self.cb = cleverbot.Cleverbot()
        self.tag = 'cleverbot'
        self.shortTag = 'cb'

    def isReadingMessages(self):
        return True

    async def readMessage(self, message):
        pass

    @styrobot.plugincommand('Sends a message to CleverBot', name='chat', parserType=commands.ParamParserType.ALL)
    async def _chat_(self, server, channel, author, text):
        self.logger.debug('[chat] [%s]: %s', author, text)
        response = self.cb.ask(text)
        self.logger.debug('[chat] [cleverbot]: %s', response)
        await self.bot.send_message(channel, response)
