from plugin import Plugin
import pafy
import asyncio
import discord

class Song:
    def __init__(self, message, song):
        self.requester = message.author
        self.channel = message.channel
        self.song = song
    
class Music(Plugin):

    async def initialize(self, bot):
        self.bot = bot
        self.songs = asyncio.Queue()
        self.play_next_song = asyncio.Event()
        self.starter = None
        self.player = None
        self.currentSong = None
        self.commands = []

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

        return commands

    def checkForCommand(self, command):
        for com in self.commands:
            if com == command:
                print('Command Found!')
                return True

        return False

    async def executeCommand(self, server, channel, author, command, parameters):
        print('Executing command: ' + command + ' with parameters: ' + parameters + ' on channel: ' + channel.name)

        if command == '!joinvoice' and parameters != '':
            check = lambda c: c.name == parameters and c.type == discord.ChannelType.voice

            chan = discord.utils.find(check, server.channels)
            if chan is None:
                print('Invalid channel name.')
                await self.bot.send_message(channel, 'Invalid channel name.')
                return

            await self.bot.join_voice_channel(chan)
            self.starter = author

        #firstWord = parameters.split(' ', 1)[0]


    def dl_song(self, message, url, name):
        video = pafy.new(url)
        audio = video.audiostreams
        songFile = audio[0].download(filepath="music/" + name + ".mp3")

    async def skip(self, message):
        self.player.stop()

        await play(message)

    async def stop(self):
        self.player.stop()

    async def play(self, message):
        if self.player is not None and self.player.is_playing():
            await self.bot.send_message(message.channel, 'Not connected to a channel.')
            return

        while True:
            if not self.bot.is_voice_connected():
                await self.bot.send_message(message.channel, 'Not connected to a channel.')
                return

            self.play_next_song.clear()
            self.currentSong = await self.songs.get()
            self.player = self.bot.voice.create_ffmpeg_player(self.currentSong.song, after=self.toggle_next_song)
            self.player.start()
            fmt = '{0.requester} is now playing "{0.song}"'
            await self.bot.send_message(self.currentSong.channel, fmt.format(self.currentSong))
            await self.play_next_song.wait()

    async def queue_song(self, message, filename):
        await self.songs.put(Song(message, filename))
        await self.bot.send_message(message.channel, '{} has been queued.'.format(filename))

    def toggle_next_song(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    def can_control_song(self, author):
        return author == self.starter or (self.currentSong is not None and author == self.currentSong.requester)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    def shutdown(self):
        print('Shutdown Music')
