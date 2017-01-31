from plugin import Plugin
import discord
import logging
import os
import pafy
import styrobot
import commands

class Trollolo(Plugin):

    async def initialize(self, bot):
        self.tag = 'troll'
        self.shortTag = 't'
        self.player = None

        if not os.path.exists('troll'):
            os.makedirs('troll')

    def _sendParser(args):
        firstSpace = args.find(' ')
        firstColon = args.find(':')

        if firstColon is -1:
            return []

        result = []

        # Parse for command args and user
        if firstSpace < firstColon and firstSpace is not -1:
            tmp = args.split(' ', 1)

            result.append(tmp[0])

            tmp = tmp[1].split(':', 1)
            result.append(tmp[0])
            result.append(tmp[1])

        # Parse just for command and user
        else:
            tmp = args.split(':', 1)
            result.append(tmp[0])
            result.append('')
            result.append(tmp[1])

        return result

    @styrobot.plugincommand('Sends the troll <command> with <args> (if any) directly to <user>.', name='send', parser=_sendParser)
    async def _send_(self, server, channel, author, command, args, user, **kwargs):
        """
           !troll send isengard:Nick Cage
           !troll send numberone runescape:Nick Cage
        """
        if command in self.parsedCommands:
            self.logger.debug('[send]: Command {} is valid, checking on user.'.format(command))
            _userid = self.bot.getUserFromName(server, user)

            if _userid is not None:
                commandStr = '!{} {}{}'.format(self.tag, command, '' if args is '' else ' ' + args)
                self.logger.debug('[send]: User {} is valid, executing command: {}'.format(_userid, commandStr))
                await self.bot._executePluginCommand(commandStr, server, channel, author, userid=_userid)
            else:
                self.logger.debug('[send]: There is no user with that name or nickname.')
                await self.bot.send_message(channel, 'There is no user with that name or nickname.')

        else:
            self.logger.debug('[send]: That is not a valid command.')
            await self.bot.send_message(channel, 'That is not a valid command.')

    async def playTroll(self, server, channel, url, filename, **kwargs):
        if 'userid' in kwargs:
            self.logger.debug('Sending {} to {}'.format(filename, kwargs['userid']))
            await self.bot.send_message(kwargs['userid'], '<{}>'.format(url))
            return

        if self.bot.is_voice_connected(server):
            if not os.path.isfile('troll/' + filename + '.mp3'):
                self.dl_song(url, filename)

            if not self.is_playing():
                voiceChannel = self.bot.voice_client_in(server)
                self.player = voiceChannel.create_ffmpeg_player('troll/'+ filename + '.mp3')
                self.player.start()
                return

        await self.bot.send_message(channel, url)

    @styrobot.plugincommand('Never gonna give you up! Never gonna let you down! Never gonna run around and desert you!', name='rickroll')
    async def _rickroll_(self, server, channel, author, **kwargs):
        """
           !troll rickroll
        """
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        await self.playTroll(server, channel, url, 'rickroll', **kwargs)

    @styrobot.plugincommand('Saruman has never sounded more beautiful', name='trololo')
    async def _trololo_(self, server, channel, author, **kwargs):
        """
           !troll trololo
        """
        url = 'https://www.youtube.com/watch?v=KaqC5FnvAEc'
        await self.playTroll(server, channel, url, 'trololo', **kwargs)

    @styrobot.plugincommand('They are taking the hobbits to isengardgardgardgagagagard', name='isengard')
    async def _isengard_(self, server, channel, author, **kwargs):
        """
           !troll isengard
        """
        url = 'https://www.youtube.com/watch?v=uE-1RPDqJAY'
        await self.playTroll(server, channel, url, 'isengard', **kwargs)

    @styrobot.plugincommand('And I said heyeayeayeayea! heyeayea! I said hey! What\'s going on?', name='heyeayea')
    async def _heyeayea_(self, server, channel, author, **kwargs):
        """
           !troll heyeayea
        """
        url = 'https://www.youtube.com/watch?v=ZZ5LpwO-An4'
        await self.playTroll(server, channel, url, 'heyeayea', **kwargs)

    @styrobot.plugincommand('Nyan nyan nyan', name='nyan')
    async def _nyan_(self, server, channel, author, **kwargs):
        """
           !troll nyan
        """
        url = 'https://www.youtube.com/watch?v=QH2-TGUlwu4'
        await self.playTroll(server, channel, url, 'nyan', **kwargs)

    @styrobot.plugincommand('*queues sax music*  We are number one! Hey!\nAvailable versions: original, runescape, synthwave, soviet', name='numberone')
    async def _numberone_(self, server, channel, author, version, **kwargs):
        """
           !troll numberone
           !troll numberone original
           !troll numberone runescape
           !troll numberone synthwave, soviet
           !troll numberone soviet
        """
        url = ''
        name = ''

        if version == '' or version.lower() == 'original':
            url = 'https://www.youtube.com/watch?v=PfYnvDL0Qcw'
            name = 'numberone'
        elif version.lower() == 'runescape':
            url = 'https://www.youtube.com/watch?v=s0H5PgnC-iA'
            name = 'numberone_runescape'
        elif version.lower() == 'synthwave':
            url = 'https://www.youtube.com/watch?v=7FkpM4FWa8A'
            name = 'numberone_synthwave'
        elif version.lower() == 'soviet':
            url = 'https://www.youtube.com/watch?v=yCrYvHBMGLY'
            name = 'numberone_soviet'
        else:
            self.logger.debug('[numberone]: The version you provided is invalid.')
            await self.bot.send_message(channel, 'The version you provided is invalid.')
            return

        await self.playTroll(server, channel, url, name, **kwargs)

    @styrobot.plugincommand('Yar har fiddle dee dee, being a pirate is alright with me! Do what you want cause a pirate is free, you are a pirate!', name='pirate')
    async def _pirate_(self, server, channel, author, **kwargs):
        """
           !troll pirate
        """
        url = 'https://www.youtube.com/watch?v=i8ju_10NkGY'
        await self.playTroll(server, channel, url, 'pirate', **kwargs)

    @styrobot.plugincommand('Yeeeeeeeeeeeee', name='yeee')
    async def _yeee_(self, server, channel, author, **kwargs):
        """
           !troll yeee
        """
        url = 'https://www.youtube.com/watch?v=q6EoRBvdVPQ'
        await self.playTroll(server, channel, url, 'yeee', **kwargs)

    @styrobot.plugincommand('Impressive... Most impressive.', name='impressive')
    async def _impressive_(self, server, channel, author, **kwargs):
        """
           !troll impressive
        """
        url = 'https://www.youtube.com/watch?v=bTlXZf5qsZI'
        await self.playTroll(server, channel, url, 'impressive', **kwargs)

    @styrobot.plugincommand('Power!!!!! **UNLIMITED POWER!!!!**', name='power')
    async def _power_(self, server, channel, author, **kwargs):
        """
           !troll power
        """
        url = 'https://www.youtube.com/watch?v=0D8i8QGgz0k'
        await self.playTroll(server, channel, url, 'power', **kwargs)

    @styrobot.plugincommand('Goood anakin, goooodd', name='goodanakin')
    async def _goodanakin_(self, server, channel, author, **kwargs):
        """
           !troll goodanakin
        """
        url = 'https://www.youtube.com/watch?v=VdFoAi_f30Q'
        await self.playTroll(server, channel, url, 'goodanakin', **kwargs)

    @styrobot.plugincommand('If the baggins loses, we eats it whole!', name='eatsitwhole')
    async def _eatsitwhole_(self, server, channel, author, **kwargs):
        """
           !troll eatsitwhole
        """
        url = 'https://www.youtube.com/watch?v=rV73aShBFgs'
        await self.playTroll(server, channel, url, 'eatsitwhole', **kwargs)

    @styrobot.plugincommand('We\'ve had one, yes, but what about second breakfast?', name='secondbreakfast')
    async def _secondbreakfast_(self, server, channel, author, **kwargs):
        """
           !troll secondbreakfast
        """
        url = 'https://www.youtube.com/watch?v=XkzvHtjnNOs'
        await self.playTroll(server, channel, url, 'secondbreakfast', **kwargs)

    @styrobot.plugincommand('TROLL IN THE DUNGEON! TROLL IN THE DUNGEON! Thought you ought to know.', name='dungeon')
    async def _dungeon_(self, server, channel, author, **kwargs):
        """
           !troll dungeon
        """
        url = 'https://www.youtube.com/watch?v=R5kPUFxXYLs'
        await self.playTroll(server, channel, url, 'dungeon', **kwargs)

    def dl_song(self, url, name):
        video = pafy.new(url)
        audio = video.audiostreams
        songFile = audio[0].download(filepath="troll/" + name + ".mp3")

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def shutdown(self):
        self.player = None
