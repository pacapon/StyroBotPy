from plugin import Plugin
import os
import shutil
import pafy
import asyncio
import discord
import styrobot
import logging
import commands

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
        self.tag = 'music'
        self.shortTag = 'm'

    @styrobot.plugincommand('Play the queued songs', name='play')
    async def _play_(self, server, channel, author):
        await self.play(channel)
        self.logger.debug('[play]: Playing the song queue')

    @styrobot.plugincommand('Pause the currently playing song', name='pause')
    async def _pause_(self, server, channel, author):
        if not self.can_control_song(author):
            fmt = 'Only the requester (<@{0.currentSong.requester.id}>) or an admin can control this song.'
            logfmt = 'Only the requester ({0.currentSong.requester}) or an admin can control this song.'

            self.logger.debug('[pause]: %s', logfmt.format(self))
            await self.send_message(channel, fmt.format(self))
            return

        if self.player.is_playing():
            self.player.pause()
            await self.bot.send_message(channel, 'Pausing song.')
            self.logger.debug('[pause]: Pausing song.')

    @styrobot.plugincommand('Resume the currently paused song', name='resume')
    async def _resume_(self, server, channel, author):
        if not self.can_control_song(author):
            fmt = 'Only the requester (<@{0.currentSong.requester.id}>) or an admin can control this song.'
            logfmt = 'Only the requester ({0.currentSong.requester}) or an admin can control this song.'

            self.logger.debug('[resume]: %s', fmt.format(self))
            await self.bot.send_message(channel, fmt.format(self))
            return

        if self.player is not None and not self.is_playing():
            self.player.resume()
            await self.bot.send_message(channel, 'Resuming song.')
            self.logger.debug('[resume]: Resuming song.')

    @styrobot.plugincommand('Skip the currently playing song', name='skip')
    async def _skip_(self, server, channel, author):
        if self.songs.qsize() <= 0:
            self.logger.debug('[skip]: Can\'t skip, 1 or less songs remaining.')
            await self.bot.send_message(channel, 'Can\'t skip, 1 or less songs remaining.')
            return

        await self.skip(channel)
        await self.bot.send_message(channel, 'Skipping song.')
        self.logger.debug('[skip]: Skipping song.')

    @styrobot.plugincommand('Stops the song queue completely. Requires admin permissions.', name='stop')
    async def _stop_(self, server, channel, author):
        if not self.bot.isAdmin(author):
            self.logger.debug('[stop]: You must be an admin to do this.')
            await self.bot.send_message(channel, 'You must be an admin to do this.')
            return

        self.logger.debug('[stop]: Stopping song queue.')
        await self.stop()

    @styrobot.plugincommand('Queue the song called <name> to be played next', name='next')
    async def _next_(self, server, channel, author, name):
        filename = 'music/' + name.strip() + '.mp3'
        self.logger.debug('[next]: Queuing song %s', filename)
        await self.queue_song(author, channel, filename)

    @styrobot.plugincommand('Download song at <url> (must be youtube) for playback using <name>', name='add')
    async def _add_(self, server, channel, author, url, name):
        self.logger.debug('[add]: Adding song [%s] at url [%s]', name, url)
        await self.addSong(channel, url, name)

    @styrobot.plugincommand('Download song at <url> (must be youtube) for playback using <name> and queue to be played next', name='addnq')
    async def _addnq_(self, server, channel, author, url, name):
        self.logger.debug('[addnq]: Adding song [%s] at url [%s]', name, url)
        filename = await self.addSong(channel, url, name)

        if filename != False:
            self.logger.debug('[addnq]: Queuing song [%s]', filename)
            await self.queue_song(author, channel, filename)

    @styrobot.plugincommand('Delete song(s) <name> <name> <...>', name='delete', parserType=commands.ParamParserType.ALL)
    async def _delete_(self, server, channel, author, names):
        if self.bot.isAdmin(author):
            names = names.split()
            try:
                for name in names:
                    filename = 'music/' + name + '.mp3'
                    os.remove(filename)
                    self.logger.debug('[delete]: Deleted %s', filename)
                    await self.bot.send_message(channel, 'Song ' + name + ' deleted')
            except OSError:
                self.logger.debug('[delete]: File %s does not exist', filename)
                await self.bot.send_message(channel, 'Unable to delete song ' + name)
            finally:
                return

        self.logger.debug('[delete]: %s, You do not have permission to do that.', author)
        await self.bot.send_message(channel, '<@' + author.id + '>, You do not have permission to do that.')

    @styrobot.plugincommand('Delete all songs', name='deleteall')
    async def _deleteall_(self, server, channel, author):
        if self.bot.isAdmin(author):
            shutil.rmtree('music/')
            os.mkdir('music/')
            self.logger.debug('Deleting all songs from the music directory')
            await self.bot.send_message(channel, 'Deleted all songs')
            return

        self.logger.debug('[delete]: %s, You do not have permission to do that.', author)
        await self.bot.send_message(channel, '<@' + author.id + '>, You do not have permission to do that.')

    @styrobot.plugincommand('Display the list of available songs to play', name='library')
    async def _library_(self, server, channel, author):
        songFiles = os.listdir('music/')
        library = ''

        if not songFiles:
            await self.bot.send_message(channel, 'No songs to display.')
            return

        for song in songFiles:
            library += song
            library += '\n'

        self.logger.debug('[songlist]: Songs: %s', library)
        await self.bot.send_message(channel, 'Songs: \n' + library)

    @styrobot.plugincommand('Display the list of queued songs', name='queue')
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
            self.dl_song(url, name)
        except:
            self.logger.error('Failed to download song: %s', name)
            await self.bot.send_message(channel, 'Failed to download song: ' + name)
            return False

        self.logger.debug('%s has been successfully added.', name)
        await self.bot.send_message(channel, name + ' has been successfully added.')

        return filename

    def dl_song(self, url, name):
        video = pafy.new(url)
        audio = video.audiostreams
        songFile = audio[0].download(filepath="music/" + name + ".mp3")

    async def skip(self, channel):
        self.player.stop()

    async def stop(self):
        while not self.songs.empty():
            self.songs.get_nowait()

        if self.player != None:
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

            if self.bot.voiceChannel is None:
                self.logger.debug('Not connected to a channel.')
                await self.bot.send_message(channel, 'Not connected to a channel.')
                return

            self.play_next_song.clear()
            self.currentSong = await self.songs.get()
            self.songNames.pop(0)

            self.player = self.bot.voiceChannel.create_ffmpeg_player(self.currentSong.song, after=self.toggle_next_song)
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
        return author == self.starter or (self.currentSong is not None and author == self.currentSong.requester) or self.bot.isAdmin(author)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def onLeaveVoiceChannel(self):
        await self.stop()

    async def shutdown(self):
        await self.stop()
        self.starter = None
        self.player = None
