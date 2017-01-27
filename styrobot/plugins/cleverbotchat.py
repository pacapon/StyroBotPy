from plugin import Plugin
import cleverbot
import logging
import styrobot
import commands
import re

class CleverBotChat(Plugin):
    async def initialize(self, bot):
        self.cb = cleverbot.Cleverbot('styrobot.py')
        self.tag = 'cleverbot'
        self.shortTag = 'cb'

    def isReadingMessages(self):
        return True

    async def readMessage(self, message):
        if message.server.me in message.mentions: 
            if len(message.mentions) == 1:
                self.logger.debug('[readMessage]: Mention of bot is found. Parsing all text after mention in message and sending to cleverbot.')

                botMessage = message.content.split('<@', 1)[1]
                botMessage = botMessage.split('>', 1)[1]

                botMessage = self.scrubMessage(botMessage)
                self.logger.debug('[readMessage]: Message content: %s', botMessage)

                await self._chat_(message.server, message.channel, message.author, botMessage)
            else:
                self.logger.debug('[readMessage]: There is more than one mention. Ignoring due to complexity.')

    @styrobot.plugincommand('Sends a message to CleverBot', name='chat', parserType=commands.ParamParserType.ALL)
    async def _chat_(self, server, channel, author, text):
        self.logger.debug('[chat] [%s]: %s', author, text)
        response = self.cb.ask(text)
        self.logger.debug('[chat] [cleverbot]: %s', response)
        await self.bot.send_message(channel, response)

    # Takes in the message's content and removes all markdown
    def scrubMessage(self, message):
        scrubbedMessage = re.findall('[^_*\-\'\"\`\~,]', message)
        self.logger.debug('Scrubbed message: %s', ''.join(scrubbedMessage).lower())

        return ''.join(scrubbedMessage).lower()

