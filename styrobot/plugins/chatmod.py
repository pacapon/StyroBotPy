from plugin import Plugin
import discord
import re
import logging
import styrobot

class ChatMod(Plugin):

    async def initialize(self, bot):
        self.bannedWords = []
        self.userWarnings = {}
        self.maxWarnings = 2 # How many warnings should a user get before action is taken
        self.tag = 'chatmod'
        self.shortTag = 'cm'

        # What action to take on a user after they've maxed out their warnings
        # Options are: kick and ban
        self.banAction = 'kick'

        self.logger.debug('This bot is part of %s servers!', str(len(self.bot.servers)))

        for server in self.bot.servers:
            settings = await self.bot.getSettingsForTag(server, self.tag)

            if 'maxwarn' in settings:
                self.maxWarnings = settings['maxwarn']
            else:
                await self.bot.modifySetting(server, self.tag, 'maxwarn', self.maxWarnings)

            if 'banact' in settings:
                self.banAction = settings['banact']
            else:
                await self.bot.modifySetting(server, self.tag, 'banact', self.banAction)

            if 'bannedWords' in settings:
                words = settings['bannedWords'][1:-1]

                if words:
                    words = words.split(', ')

                    for word in words:
                        self.bannedWords.append(word[1:-1])
            else:
                await self.bot.modifySetting(server, self.tag, 'bannedWords', '')

    @styrobot.plugincommand('Shows the list of banned words', name='showbanned')
    async def _showbanned_(self, server, channel, author):
        """
           !chatmod showbanned
        """
        if len(self.bannedWords) > 0:
            words = ''
            for word in self.bannedWords:
                words += word + '\n'

            self.logger.debug('[showbanned]: %s', words)
            await self.bot.send_message(channel, words)
        else:
            await self.bot.send_message(channel, 'There are currently no banned words.')
            self.logger.debug('[showbanned]: There are currently no banned words.')

    @styrobot.plugincommand('Show the current settings for the chat mod plugin', name='settings')
    async def _settings_(self, server, channel, author):
        """
           !chatmod settings
        """
        self.logger.debug('[cmsettings]: Max Warnings: %s  Ban Action: %s', str(self.maxWarnings), self.banAction)
        await self.bot.send_message(channel, 'Max Warnings: ' + str(self.maxWarnings) + '\nBan Action: ' + self.banAction)

    @styrobot.plugincommand('Set the max number of warnings to <number>', name='setmaxwarn')
    async def _setmaxwarn_(self, server, channel, author, number):
        """
           !chatmod setmaxwarn <number>
        """
        if int(number) < 0:
            self.logger.debug('[cmmaxwarn]: You can\'t have negative max warnings.')
            await self.bot.send_message(channel, 'You can\'t have negative max warnings.')
        else:
            self.maxWarnings = int(number)
            await self.bot.modifySetting(server, self.tag, 'maxwarn', number)

            self.logger.debug('[cmmaxwarn]: Max Warnings have been set to: %s', str(number))
            await self.bot.send_message(channel, 'Max Warnings have been set to: ' + str(number))

    @styrobot.plugincommand('Change the action to take when a player has hit their max warnings (kick, ban)', name='setbanact')
    async def _setbanact_(self, server, channel, author, action):
        """
           !chatmod setbanact kick
           !chatmod setbanact ban
        """
        if action == 'kick' or action == 'ban':
            self.banAction = action
            await self.bot.modifySetting(server, self.tag, 'banact', action)

            self.logger.debug('[cmbanact]: Ban Action has been set to: %s', action)
            await self.bot.send_message(channel, 'Ban Action has been set to: ' + action)
        else:
            self.logger.debug('[cmbanact]: Invalid Ban Action. Please use \'kick\' or \'ban\'')
            await self.bot.send_message(channel, 'Invalid Ban Action. Please use \'kick\' or \'ban\'')

    @styrobot.plugincommand('Check your current warning status', name='status')
    async def _status_(self, server, channel, author):
        """
           !chatmod status
        """
        if author.name in self.userWarnings:
            self.logger.debug('[cmstatus]: %s, you have %s warnings.', author, str(self.userWarnings[author.name]))
            await self.bot.send_message(channel, '<@' + author.id + '>, you have ' + str(self.userWarnings[author.name]) + ' warnings.')

        else:
            self.logger.debug('[cmstatus]: %s, you have been given no warnings yet.', author)
            await self.bot.send_message(channel, '<@' + author.id+ '>, you have been given no warnings yet.')

    @styrobot.plugincommand('Adds <word> to the list of banned words', name='ban')
    async def _ban_(self, server, channel, author, word):
        """
           !chatmod ban <word>
        """
        firstWord = self.scrubMessage(word)

        if not firstWord:
            self.logger.debug('[!banword]: Cannot ban an empty string')
            await self.bot.send_message(channel, 'You must specify a word to ban!')
            return

        if not firstWord in self.bannedWords:
            self.bannedWords.append(firstWord)
            await self.updateBannedWords(server)

            self.logger.debug('[!banword]: Banning word: %s', firstWord)
            await self.bot.send_message(channel, 'Banning word: ' + firstWord)

    @styrobot.plugincommand('Removes <word> from the list of banned words', name='unban')
    async def _unban_(self, server, channel, author, word):
        """
           !chatmod unban <word>
        """
        firstWord = self.scrubMessage(word)

        if firstWord in self.bannedWords:
            self.bannedWords.remove(firstWord)
            await self.updateBannedWords(server)

            self.logger.debug('[!unbanword]: Unbanning word: %s', firstWord)
            await self.bot.send_message(channel, 'Unbanning word: ' + firstWord)

        else:
            self.logger.debug('[!unbanword]: This word is not banned.')
            await self.bot.send_message(channel, 'This word is not banned.')

    async def updateBannedWords(self, server):
        await self.bot.modifySetting(server, self.tag, 'bannedWords', str(self.bannedWords))

    def isReadingMessages(self):
        return True

    async def readMessage(self, message):
        self.logger.debug('Reading message!')
        scrubbed = self.scrubMessage(message.content)

        if not self.bannedWords:
            return

        for word in self.bannedWords:
            if word in scrubbed:
                # TODO: improve this so people can't just bypass the moderating
                if message.content.startswith('!'):
                    return

                if message.author.name in self.userWarnings:
                    self.userWarnings[message.author.name] += 1

                    if self.userWarnings[message.author.name] > int(self.maxWarnings):
                        await self.applyAction(message.author, message.channel)

                    elif self.userWarnings[message.author.name] == int(self.maxWarnings):
                        await self.bot.send_message(message.channel, 'Watch your language, <@' + message.author.id + '>. This is your final warning.')
                        self.logger.debug('%s has used the banned word: %s', message.author, word)
                    else:
                        await self.bot.send_message(message.channel, 'Watch your language, <@' + message.author.id + '>. You have been warned.')
                        self.logger.debug('%s has used the banned word: %s', message.author, word)

                else:
                    self.userWarnings[message.author.name] = 1

                    await self.bot.send_message(message.channel, 'Watch your language, <@' + message.author.id + '>. You have been warned.')
                    self.logger.debug('%s has used the banned word: %s', message.author, word)

    # Takes in the message's content and removes all markdown so it doesn't
    # screw up the detection as much
    def scrubMessage(self, message):
        scrubbedMessage = re.findall('[^_*\-\'\"\`\~,]', message)
        self.logger.debug('Scrubbed message: %s', ''.join(scrubbedMessage).lower())

        return ''.join(scrubbedMessage).lower()

    async def applyAction(self, user, channel):
        if self.banAction == 'kick':
            self.logger.debug('Kicking %s for bad language.', user.name)
            await self.bot.send_message(channel, 'Kicking <@' + user.id + '> for bad language.')

            await self.bot.kick(user)

        elif self.banAction == 'ban':
            self.logger.debug('Banning %s for bad language.', user.name)
            await self.bot.send_message(channel, 'Banning <@' + user.id + '> for bad language.')

            await self.bot.ban(user)
