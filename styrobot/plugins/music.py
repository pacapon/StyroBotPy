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
        self.songs = asyncio.Queue()
        self.songNames = []
        self.play_next_song = asyncio.Event()
        self.starter = None
        self.player = None
        self.currentSong = None
        self.voiceChannel = None
        self.tag = 'music'
        self.shortTag = 'm'

        self.commands.append('<join><1>(name)<Join voice channel with given name>')
        self.commands.append('<leave><0><Leave the current voice channel>')
        self.commands.append('<play><0><Play the queued songs>')
        self.commands.append('<pause><0><Pause the currently playing song>')
        self.commands.append('<resume><0><Resume the currently paused song>')
        self.commands.append('<skip><0><Skip the currently playing song>')
        self.commands.append('<next><1>(name)<Queue the song called [name] to be played next>')
        self.commands.append('<add><2>(url, name)<Download song at [url] (must be youtube) for playback using [name]>')
        self.commands.append('<addnq<2>(url, name)<Download song at [url] (must be youtube) for playback using [name] and queue to be played next')
        self.commands.append('<songlist><0><Display the list of available songs to play>')
        self.commands.append('<queue><0><Display the list of queued songs>')

    async def _join_(self, server, channel, author, name):
        check = lambda c: c.name == name and c.type == discord.ChannelType.voice

        chan = discord.utils.find(check, server.channels)
        if chan is None:
            self.logger.debug('[join]: Invalid channel name.')
            await self.bot.send_message(channel, 'Invalid channel name.')
            return

        self.voiceChannel = await self.bot.join_voice_channel(chan)
        self.starter = author

    async def _leave_(self, server, channel, author):
        if not self.can_control_song(author):
            return
        self.starter = None

        self.logger.debug('[leave]: Leaving voice channel %s', self.voiceChannel.channel.name)
        await self.voiceChannel.disconnect()
        self.voiceChannel = None

    async def _play_(self, server, channel, author):
        await self.play(channel)
        self.logger.debug('[play]: Playing the song queue')

    async def _pause_(self, server, channel, author):
        if not self.can_control_song(author):
            fmt = 'Only the requester (<@{0.currentSong.requester.id}>) can control this song.'
            logfmt = 'Only the requester ({0.currentSong.requester}) can control this song.'

            self.logger.debug('[pause]: %s', logfmt.format(self))
            await self.send_message(channel, fmt.format(self))
            return

        if self.player.is_playing():
            self.player.pause()
            await self.bot.send_message(channel, 'Pausing song.')
            self.logger.debug('[pause]: Pausing song.')

    async def _resume_(self, server, channel, author):
        if not self.can_control_song(author):
            fmt = 'Only the requester (<@{0.currentSong.requester.id}>) can control this song.'
            logfmt = 'Only the requester ({0.currentSong.requester}) can control this song.'

            self.logger.debug('[resume]: %s', fmt.format(self))
            await self.bot.send_message(channel, fmt.format(self))
            return

        if self.player is not None and not self.is_playing():
            self.player.resume()
            await self.bot.send_message(channel, 'Resuming song.')
            self.logger.debug('[resume]: Resuming song.')

    async def _skip_(self, server, channel, author):
        if self.songs.qsize() <= 0:
            self.logger.debug('[skip]: Can\'t skip, 1 or less songs remaining.')
            await self.bot.send_message(channel, 'Can\'t skip, 1 or less songs remaining.')
            return

        await self.skip(channel)
        await self.bot.send_message(channel, 'Skipping song.')
        self.logger.debug('[skip]: Skipping song.')

    async def _next_(self, server, channel, author, name):
        filename = 'music/' + name.strip() + '.mp3'
        self.logger.debug('[next]: Queuing song %s', filename)
        await self.queue_song(author, channel, filename)

    async def _add_(self, server, channel, author, url, name):
        self.logger.debug('[add]: Adding song [%s] at url [%s]', name, url)
        await self.addSong(channel, url, name)
         
    async def _addnq_(self, server, channel, author, url, name):
        self.logger.debug('[addnq]: Adding song [%s] at url [%s]', name, url)
        filename = await self.addSong(channel, url, name)

        if filename != False:
            self.logger.debug('[addnq]: Queuing song [%s]', filename)
            await self.queue_song(author, channel, filename)


    async def _songlist_(self, server, channel, author):
        songFiles = os.listdir('music/')
        songList = '' 

        for song in songFiles:
            songList += song
            songList += '\n'

        self.logger.debug('[songlist]: Songs: %s', songList)
        await self.bot.send_message(channel, 'Songs: \n' + songList)

    async def _queue_(self, server, channel, author):
        if len(self.songNames) == 0:
            self.logger.debug('[queue]: There are no queued songs.')
            await self.bot.send_message(channel, 'There are no queued songs.')
            return

        songList = ''

        for song in self.songNames:
            songList += song + '\n'

        self.logger.debug('[queue]: Queued Songs: %s', songList)
        await self.bot.send_message(channel, 'Queued Songs: \n' + songList)

    async def addSong(self, channel, url, name):
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

