from plugin import Plugin
import discord
import styrobot
import random
import logging

class Quotes(Plugin):

    async def initialize(self, bot):
        self.bot = bot
        self.commands = []
        self.channelName = 'quotes'
        self.logger = logging.getLogger('styrobot.quotes')

        self.commands.append('!quote')
        self.commands.append('!quotechannel')

        self.logger.debug('This Bot is part of %s servers!', str(len(self.bot.servers)))

        for server in self.bot.servers:
            settings = await self.bot.getSettings(server)

            if 'channame' in settings:
                self.channelName = settings['channame']
            else:
                await self.bot.modifySetting(server, 'channame', self.channelName)

        self.channel = discord.utils.get(server.channels, name=self.channelName, type=discord.ChannelType.text)

        if self.channel == None:
            self.logger.debug('No quotes channel found, creating channel')
            self.channel = await self.bot.create_channel(server, self.channelName)

                
    def getCommands(self):
        commands = []

        commands.append('**!quote**   - Say a random quote from the quotes channel')
        commands.append('**!quotechannel <name>**   - Changes the channel to use for quotes to the channel called <name>')

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                self.logger.debug('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters):
        if command == '!quote':
            quotes = []
            async for message in self.bot.logs_from(self.channel, limit=1000000):
                quotes.append(message)

            if len(quotes) == 0:
                self.logger.debug('[!quote]: There are no quotes in the %s channel!', self.channelName)
                await self.bot.send_message(channel, 'There are no quotes in the ' + self.channelName + ' channel!')
                return

            randQuote = quotes[random.randint(0, len(quotes) - 1)]

            self.logger.debug('[!quote]: %s', randQuote.content)
            await self.bot.send_message(channel, randQuote.content)

        elif command == '!quotechannel' and parameters != '':
            firstWord = parameters.split(' ', 1)[0]

            newChan = discord.utils.get(server.channels, name=firstWord, type=discord.ChannelType.text)

            if newChan != None:
                self.channel = newChan 

                await self.bot.modifySetting(server, 'channame', firstWord)

                self.logger.debug('[!quotechannel]: Quotes will now be taken from channel: %s', firstWord)
                await self.bot.send_message(channel, 'Quotes will now be taken from channel: ' + firstWord)

            else:
                self.logger.debug('[!quotechannel]: There is no channel with that name.')
                await self.bot.send_message(channel, 'There is no channel with that name.')
