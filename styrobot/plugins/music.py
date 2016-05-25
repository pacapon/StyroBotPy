from plugin import Plugin
import os
import pafy
import asyncio
import discord
import logging

class Song:
    def __init__(self, author, channel, song):
        self.requester = author
        self.channel = channel
        self.song = song
    
class Music(Plugin):

    async def initialize(self, bot):
        self.bot = bot
        self.songs = asyncio.Queue()
        self.songNames = []
        self.play_next_song = asyncio.Event()
        self.starter = None
        self.player = None
        self.currentSong = None
        self.voiceChannel = None
        self.commands = []
        self.logger = logging.getLogger('styrobot.music')

        self.commands.append('!joinvoice')
        self.commands.append('!leave')
        self.commands.append('!play')
        self.commands.append('!pause')
        self.commands.append('!resume')
        self.commands.append('!skip')
        self.commands.append('!next')
        self.commands.append('!addsong')
        self.commands.append('!addnq')
        self.commands.append('!songlist')
        self.commands.append('!songqueue')

    def getCommands(self):
        commands = []

        commands.append('**!joinvoice <name>**   - Join voice channel with given name')
        commands.append('**!leave**   - Leave the current voice channel')
        commands.append('**!play**   - Play the queued songs')
        commands.append('**!pause**   - Pause the currently playing song') 
        commands.append('**!resume**   - Resume the currently paused song') 
        commands.append('**!skip**   - Skip the currently playing song') 
        commands.append('**!next <name>**   - Queue the song called <name> to be played next') 
        commands.append('**!addsong <url> <name>**   - Download song at <url> for playback using <name>') 
        commands.append('**!addnq <url> <name>**   - Download song at <url> for playback using <name> and queue to be played next') 
        commands.append('**!songlist**   - Display the list of available songs to play') 
        commands.append('**!songqueue**   - Display the list of queued songs') 

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                self.logger.debug('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters): 
        if command == '!joinvoice' and parameters != '':
            check = lambda c: c.name == parameters and c.type == discord.ChannelType.voice

            chan = discord.utils.find(check, server.channels)
            if chan is None:
                self.logger.debug('[!joinvoice]: Invalid channel name.')
                await self.bot.send_message(channel, 'Invalid channel name.')
                return

            self.voiceChannel = await self.bot.join_voice_channel(chan)
            self.starter = author

        elif command == '!leave':
            if not self.can_control_song(author):
                return
            self.starter = None

            self.logger.debug('[!leave]: Leaving voice channel %s', self.voiceChannel.channel.name)
            await self.voiceChannel.disconnect()
            self.voiceChannel = None

        elif command == '!play':
            await self.play(channel)
            self.logger.debug('[!play]: Playing the song queue')

        elif command == '!pause':
            if not self.can_control_song(author):
                fmt = 'Only the requester (<@{0.currentSong.requester.id}>) can control this song.'
                logfmt = 'Only the requester ({0.currentSong.requester}) can control this song.'

                self.logger.debug('[!pause]: %s', logfmt.format(self))
                await self.send_message(channel, fmt.format(self))
                return

            if self.player.is_playing():
                self.player.pause()
                await self.bot.send_message(channel, 'Pausing song.')
                self.logger.debug('[!pause]: Pausing song.')

        elif command == '!resume':
            if not self.can_control_song(author):
                fmt = 'Only the requester (<@{0.currentSong.requester.id}>) can control this song.'
                logfmt = 'Only the requester ({0.currentSong.requester}) can control this song.'

                self.logger.debug('[!resume]: %s', fmt.format(self))
                await self.bot.send_message(channel, fmt.format(self))
                return

            if self.player is not None and not self.is_playing():
                self.player.resume()
                await self.bot.send_message(channel, 'Resuming song.')
                self.logger.debug('[!resume]: Resuming song.')

        elif command == '!skip':
            if self.songs.qsize() <= 0:
                self.logger.debug('[!skip]: Can\'t skip, 1 or less songs remaining.')
                await self.bot.send_message(channel, 'Can\'t skip, 1 or less songs remaining.')
                return

            await self.skip(channel)
            await self.bot.send_message(channel, 'Skipping song.')
            self.logger.debug('[!skip]: Skipping song.')

        elif command == '!next' and parameters != '':
            filename = 'music/' + parameters.strip() + '.mp3'
            self.logger.debug('[!next]: Queuing song %s', filename)
            await self.queue_song(author, channel, filename)

        elif command == '!addsong' and parameters != '':
            self.logger.debug('[!addsong]: Adding song %s', parameters)
            await self.addSong(channel, parameters)
            
        elif command == '!addnq' and parameters != '':
            self.logger.debug('[!addnq]: Adding song %s', parameters)
            filename = await self.addSong(channel, parameters)

            if filename != False:
                self.logger.debug('[!addnq]: Queuing song %s', filename)
                await self.queue_song(author, channel, filename)

        elif command == '!songlist':
            songFiles = os.listdir('music/')
            songList = '' 

            for song in songFiles:
                songList += song
                songList += '\n'

            self.logger.debug('[!songlist]: Songs: %s', songList)
            await self.bot.send_message(channel, 'Songs: \n' + songList)

        elif command == '!songqueue':

            if len(self.songNames) == 0:
                self.logger.debug('[!songqueue]: There are no queued songs.')
                await self.bot.send_message(channel, 'There are no queued songs.')
                return

            songList = ''

            for song in self.songNames:
                songList += song + '\n'

            self.logger.debug('Queued Songs: %s', songList)
            await self.bot.send_message(channel, 'Queued Songs: \n' + songList)

    async def addSong(self, channel, parameters):
        args = parameters.split()
        url = args[0]
        name = args[1]
        filename = 'music/' + name + '.mp3'

        try:
            self.dl_song(channel, url, name)
        except:
            self.logger.error('Failed to download song: %s', name)
            await self.bot.send_message(channel, 'Failed to download song: ' + name)
            return False 

        self.logger.debug('%s has been successfully added.', name)
        await self.bot.send_message(channel, name + ' has been successfully added.')

        return filename

    def dl_song(self, channel, url, name):
        video = pafy.new(url)
        audio = video.audiostreams
        songFile = audio[0].download(filepath="music/" + name + ".mp3")
        
    async def skip(self, channel):
        self.player.stop()

    async def stop(self):
        self.player.stop()

    async def play(self, channel):
        if self.player is not None and self.player.is_playing():
            self.logger.debug('Already playing.')
            await self.bot.send_message(channel, 'Already playing.')
            return

        if self.songs.empty():
            self.logger.debug('There are no songs in the queue.')
            await self.bot.send_message(channel, 'There are no songs in the queue.')
            return

        while True:
            if not self.bot.is_voice_connected(channel.server):
                self.logger.debug('Not connected to a channel.')
                await self.bot.send_message(channel, 'Not connected to a channel.')
                return

            if self.songs.empty():
                self.logger.debug('Finished playing song queue.')
                await self.bot.send_message(channel, 'Finished playing song queue.')
                return

            if self.voiceChannel is None:
                self.logger.debug('Not connected to a channel.')
                await self.bot.send_message(channel, 'Not connected to a channel.')
                return
            
            self.play_next_song.clear()
            self.currentSong = await self.songs.get()
            self.songNames.pop(0)

            self.player = self.voiceChannel.create_ffmpeg_player(self.currentSong.song, after=self.toggle_next_song)
            self.player.start()
            fmt = '<@{0.requester.id}> is now playing "{0.song}"'
            logfmt = '{0.requester} is now playing "{0.song}"'

            self.logger.debug('%s', logfmt.format(self.currentSong))
            await self.bot.send_message(self.currentSong.channel, fmt.format(self.currentSong))
            await self.play_next_song.wait()

    def getVoiceClient(self, channel):
        for voice in self.bot.voice_clients:
            if voice.channel is channel:
                return voice

        return None

    async def queue_song(self, author, channel, filename):
        await self.songs.put(Song(author, channel, filename))
        self.songNames.append(filename)

        self.logger.debug('%s has been queued.', filename)
        await self.bot.send_message(channel, '{} has been queued.'.format(filename))

    def toggle_next_song(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    def can_control_song(self, author):
        return author == self.starter or (self.currentSong is not None and author == self.currentSong.requester)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def shutdown(self):
        self.starter = None
        self.player = None
        if self.voiceChannel != None:
            await self.voiceChannel.disconnect()

