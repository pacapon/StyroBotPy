from plugin import Plugin
import discord
import styrobot
import random
import logging

class Test(Plugin):

    async def initialize(self, bot):
        self.channelName = 'quotes'
        self.tag = 'quotes'
        self.shortTag = 'q'

        self.commands.append('<quote><0><Say a random quote from the quotes channel>')
        self.commands.append('<channel><0><Says which channel is being used for quotes>')
        self.commands.append('<setchannel><1>(name)<Changes the channel to use for quotes to the channel called [name]>')
        self.commands.append('<add><*>(text)<Adds the text as a quote>')
        self.commands.append('<create><2>(quote,quoter)<Creates a quote>')

        self.logger.debug('This Bot is part of %s servers!', str(len(self.bot.servers)))

        for server in self.bot.servers:
            settings = await self.bot.getSettingsForTag(server, self.tag)

            if 'channame' in settings:
                self.channelName = settings['channame']
            else:
                await self.bot.modifySetting(server, self.tag, 'channame', self.channelName)

        self.channel = discord.utils.get(server.channels, name=self.channelName, type=discord.ChannelType.text)

        if self.channel == None:
            self.logger.debug('No quotes channel found, creating channel')
            self.channel = await self.bot.create_channel(server, self.channelName)

    async def _quote_(self, server, channel, author):
        quotes = []
        async for message in self.bot.logs_from(self.channel, limit=1000000):
            quotes.append(message)

        if len(quotes) == 0:
            self.logger.debug('[quote]: There are no quotes in the %s channel!', self.channelName)
            await self.bot.send_message(channel, 'There are no quotes in the ' + self.channelName + ' channel!')
            return

        randQuote = quotes[random.randint(0, len(quotes) - 1)]

        self.logger.debug('[quote]: %s', randQuote.content)
        await self.bot.send_message(channel, randQuote.content)

    async def _channel_(self, server, channel, author):
        self.logger.debug('[channel]: The current quote channel is: %s', self.channelName)
        await self.bot.send_message(channel, 'The current quote channel is: ' + self.channelName)

    async def _setchannel_(self, server, channel, author, channame):
        self.logger.debug('[setchannel]: Finding channel with name [%s]', channame)
        newChan = discord.utils.get(server.channels, name=channame, type=discord.ChannelType.text)

        if newChan != None:
            self.channel = newChan 
            self.channelName = channame

            await self.bot.modifySetting(server, self.tag, 'channame', channame)

            self.logger.debug('[setchannel]: Quotes will now be taken from channel: %s', channame)
            await self.bot.send_message(channel, 'Quotes will now be taken from channel: ' + channame)

        else:
            self.logger.debug('[setchannel]: There is no channel with that name.')
            await self.bot.send_message(channel, 'There is no channel with that name.')

    async def _add_(self, server, channel, author, text):
        print('[add]: ', text)

    async def _create_(self, server, channel, author, quote, quoter):
        print('[create]: ', quote, ' - ', quoter)
