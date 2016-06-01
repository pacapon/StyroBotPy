from plugin import Plugin
import cleverbot
import logging

class CleverBotChat(Plugin):
    async def initialize(self, bot):
        self.cb = cleverbot.Cleverbot()
        self.tag = 'cleverbotchat'
        self.shortTag = 'cb'
        
        self.commands.append('<chat><*>(text)<Sends a message to CleverBot>')

    async def _chat_(self, server, channel, author, text):
        self.logger.debug('[chat] [%s]: %s', author, text)
        response = self.cb.ask(text)
        self.logger.debug('[chat] [cleverbot]: %s', response)
        await self.bot.send_message(channel, response)
