import discord
import asyncio
import pafy
import os
import cleverbot
import random

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

client = discord.Client()

class Song:
    def __init__(self, message, song):
        self.requester = message.author
        self.channel = message.channel
        self.song = song

def dl_song(self, message, url, name):
    video = pafy.new(url)
    audio = video.audiostreams
    songFile = audio[0].download(filepath="music/" + name + ".mp3")

async def skip(self, message):
    self.player.stop()
    
    await play(self, message)

async def stop(self):
    self.player.stop()

async def play(self, message):
    if self.player is not None and self.player.is_playing():
        await self.send_message(message.channel, 'Already playing.')
        return

    while True:
        if not self.is_voice_connected():
            await self.send_message(message.channel, 'Not connected to a channel.')
            return

        self.play_next_song.clear()
        self.current = await self.songs.get()
        self.player = self.voice.create_ffmpeg_player(self.current.song, after=self.toggle_next_song)
        self.player.start()
        fmt = '{0.requester} is now playing "{0.song}"'
        await self.send_message(self.current.channel, fmt.format(self.current))
        await self.play_next_song.wait()

async def queue_song(self, message, filename):
    await self.songs.put(Song(message, filename))
    await self.send_message(message.channel, '{} has been queued.'.format(filename))

class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.songs = asyncio.Queue()
        self.play_next_song = asyncio.Event()
        self.starter = None
        self.player = None
        self.current = None
        self.cb = cleverbot.Cleverbot()

    def toggle_next_song(self):
        self.loop.call_soon_threadsafe(self.play_next_song.set)

    def can_control_song(self, author):
        return author == self.starter or (self.current is not None and author == self.current.requester)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('-----------')


    async def on_message(self, message):
        if message.author == self.user:
            return

        if 'poop' in message.content:
            fmt = '[Moving user {0.author} to AFK for using a banned word.]'
            check = lambda c: c.name == 'AFK' and c.type == discord.ChannelType.voice

            channel = discord.utils.find(check, message.server.channels)
            await self.move_member(message.author, channel)
            await self.send_message(message.channel, fmt.format(message))
        
        if message.content.startswith('!hello'):
            await self.send_message(message.channel, 'Hello World!')
        elif message.content.startswith('!joinvoice'):
            channel_name = message.content[10:].strip()
            check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice

            channel = discord.utils.find(check, message.server.channels)
            if channel is None:
                await self.send_message(message.channel, 'Invalid channel name.')

            await self.join_voice_channel(channel)
            self.starter = message.author
        elif message.content.startswith('!leave'):
            if not self.can_control_song(message.author):
                return
            self.starter = None
            await self.voice.disconnect()
        elif message.content.startswith('!pause'):
            if not self.can_control_song(message.author):
                fmt = 'Only the requester ({0.current.requester}) can control this song.'
                await self.send_message(message.channel, fmt.format(self))

            if self.player.is_playing():
                self.player.pause()
        elif message.content.startswith('!resume'):
            if not self.can_control_song(message.author):
                fmt = 'Only the requester ({0.current.requester}) can control this song.'
                await self.send_message(message.channel, fmt.format(self))

            if self.player is not None and not self.is_playing():
                self.player.resume()
        elif message.content.startswith('!next'):
            filename = 'music/' + message.content[5:].strip() + '.mp3'
            await queue_song(self, message, filename)
        elif message.content.startswith('!play'):
            await play(self, message)
        elif message.content.startswith('!addsong'):
            args = message.content.split()
            url = args[1]
            name = args[2]
            dl_song(self, message, url, name);          
        elif message.content.startswith('!addnq'):
            args = message.content.split()
            url = args[1]
            name = args[2]
            filename = 'music/' + name + '.mp3'
            dl_song(self, message, url, name)
            await queue_song(self, message, filename)
        elif message.content.startswith('!songlist'):
            songFiles = os.listdir('music/')
            songList = ""
            for song in songFiles:
                songList += song
                songList += "\n"
            await self.send_message(message.channel, 'Songs: \n' + songList)
        elif message.content.startswith('!skip'):
            if self.songs.qsize() <= 0:
                await self.send_message(message.channel, 'Cannot skip, 1 or less songs remaining.')
                return
            await self.send_message(message.channel, 'Skipping song.')
            await skip(self, message)
        elif message.content.startswith('!chat'):
            question = message.content[5:].strip()
            response = self.cb.ask(question)
            await self.send_message(message.channel, response)
        elif message.content.startswith('!f14'):
            await self.send_file(message.channel, 'images/f14.jpg')
        elif message.content.startswith('!changebotname'):
            newName = message.content[14:].strip()
            await self.edit_profile('nahimgucci', username=newName)
  
styroBot = Bot()
f = open('credentials.txt', 'r')
creds = f.read().splitlines()
email = creds[0]
password = creds[1]
f.close()
styroBot.run(email, password)
