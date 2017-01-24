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

    @styrobot.plugincommand('Rick Rolls the person by sending them the video privately', name='rickroll', parserType=commands.ParamParserType.ALL)
    async def _rickroll_(self, server, channel, author, username):
        user = None

        for member in server.members:
            if member.display_name == username:
                user = member
                break

        if not user:
            user = discord.utils.get(server.members, name=username)

        if user:
            self.logger.debug('Rick Rolling %s', user)
            await self.bot.send_message(user, '<https://www.youtube.com/watch?v=dQw4w9WgXcQ>')
        else:
            self.logger.debug('There is no user with this name.')
            await self.bot.send_message(channel, 'There is no user with this name.')

    async def playTroll(self, server, channel, url, filename):
        if self.bot.is_voice_connected(server):
            if not os.path.isfile('troll/' + filename + '.mp3'):
                self.dl_song(url, filename)

            if not self.is_playing():
                voiceChannel = self.bot.voice_client_in(server)
                self.player = voiceChannel.create_ffmpeg_player('troll/'+ filename + '.mp3')
                self.player.start()
                return

        await self.bot.send_message(channel, url)

    @styrobot.plugincommand('Never gonna give you up! Never gonna let you down! Never gonna run around and desert you!', name='nevergonna')
    async def _nevergonna_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        await self.playTroll(server, channel, url, 'nevergonna')

    @styrobot.plugincommand('Saruman has never sounded more beautiful', name='trololo')
    async def _trololo_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=KaqC5FnvAEc'
        await self.playTroll(server, channel, url, 'trololo')

    @styrobot.plugincommand('They are taking the hobbits to isengardgardgardgagagagard', name='isengard')
    async def _isengard_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=uE-1RPDqJAY'
        await self.playTroll(server, channel, url, 'isengard')

    @styrobot.plugincommand('And I said heyeayeayeayea! heyeayea! I said hey! What\'s going on?', name='heyeayea')
    async def _heyeayea_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=ZZ5LpwO-An4'
        await self.playTroll(server, channel, url, 'heyeayea')

    @styrobot.plugincommand('Nyan nyan nyan', name='nyan')
    async def _nyan_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=QH2-TGUlwu4'
        await self.playTroll(server, channel, url, 'nyan')

    @styrobot.plugincommand('*queues sax music*  We are number one! Hey!\nAvailable versions: original, runescape, synthwave, soviet', name='numberone')
    async def _numberone_(self, server, channel, author, version):
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

        await self.playTroll(server, channel, url, name)

    @styrobot.plugincommand('Yar har fiddle dee dee, being a pirate is alright with me! Do what you want cause a pirate is free, you are a pirate!', name='pirate')
    async def _pirate_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=i8ju_10NkGY'
        await self.playTroll(server, channel, url, 'pirate')

    @styrobot.plugincommand('Yeeeeeeeeeeeee', name='yeee')
    async def _yeee_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=q6EoRBvdVPQ'
        await self.playTroll(server, channel, url, 'yeee')

    @styrobot.plugincommand('Impressive... Most impressive.', name='impressive')
    async def _impressive_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=bTlXZf5qsZI'
        await self.playTroll(server, channel, url, 'impressive')

    @styrobot.plugincommand('Power!!!!! **UNLIMITED POWER!!!!**', name='power')
    async def _power_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=0D8i8QGgz0k'
        await self.playTroll(server, channel, url, 'power')

    @styrobot.plugincommand('Goood anakin, goooodd', name='goodanakin')
    async def _goodanakin_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=VdFoAi_f30Q'
        await self.playTroll(server, channel, url, 'goodanakin')

    @styrobot.plugincommand('If the baggins loses, we eats it whole!', name='eatsitwhole')
    async def _eatsitwhole_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=rV73aShBFgs'
        await self.playTroll(server, channel, url, 'eatsitwhole')

    @styrobot.plugincommand('We\'ve had one, yes, but what about second breakfast?', name='secondbreakfast')
    async def _secondbreakfast_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=XkzvHtjnNOs'
        await self.playTroll(server, channel, url, 'secondbreakfast')

    def dl_song(self, url, name):
        video = pafy.new(url)
        audio = video.audiostreams
        songFile = audio[0].download(filepath="troll/" + name + ".mp3")

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def shutdown(self):
        self.player = None
