import discord
import asyncio
import pafy
import os
import random
from yapsy.PluginManager import PluginManager
from plugin import Plugin

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
        #self.cb = cleverbot.Cleverbot()

        # Create Plugin Manager
        self.pluginManager = PluginManager(categories_filter={"Plugins": Plugin})
        self.pluginManager.setPluginPlaces(["plugins"])

        # Load Plugins
        self.pluginManager.locatePlugins()
        self.pluginManager.loadPlugins()

        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            print('xxxx')
            plugin.plugin_object.initialize()

    def toggle_next_song(self):
        self.loop.call_soon_threadsafe(self.play_next_song.set)

    def can_control_song(self, author):
        return author == self.starter or (self.current is not None and author == self.current.requester)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    def getHelp(self):
        helpStr = 'Basic Commands:\n'
        helpStr += '!hello   - Say Hello\n'
        helpStr += '!f14   - Create an F14!\n'
        helpStr += '!changebotname <name>   - Change the name of the bot to <name>\n'
        helpStr += '!shutdown   - Shutdown the bot (requires server admin permissions)\n'

        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            commands = plugin.plugin_object.getCommands()

            helpStr += '\n' + plugin.name + ' Commands:\n'

            for com in commands:
                helpStr += com + '\n'

        #helpStr += '!joinvoice <name>               - Join voice channel with given name\n'
        #helpStr += '!leave                                      - Leave the current voice channel\n'
        #helpStr += '!pause                                     - Pause the currently playing song\n'
        #helpStr += '!resume                                  - Resume the currently paused song\n'
        #helpStr += '!next <songname>              - Queue the song to be played next\n'
        #helpStr += '!play                                        - Play the qued songs\n'
        #helpStr += '!addsong <url> <name>    - Download song for playback\n'
        #helpStr += '!addnq <url> <name>        - Download song for playback and queue to be played next\n'
        #helpStr += '!songlist                                  - Display the current song playlist\n'
        #helpStr += '!skip                                        - Skip the currently playing song\n'
        return helpStr

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('-----------')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # We do something special with basic built-in commands 
        # because we don't want plugins using these
        if (message.content.startswith('!help')):
            await self.send_message(message.channel, self.getHelp())
            return
        elif message.content.startswith('!shutdown'):
            for role in message.author.roles:
                if role.permissions.manage_roles: # Change manage_roles if you want a different permission level to be able to do this
                    await self.logout()
                    break
            return 
        elif message.content.startswith('!hello'):
            await self.send_message(message.channel, 'Hello World!')
            return
        elif message.content.startswith('!f14'):
            await self.send_file(message.channel, 'images/f14.jpg')
            return
        elif message.content.startswith('!changebotname'):
            newName = message.content[14:].strip()
            await self.edit_profile(password, username=newName)
            return

        command = ''
        parameters = ''
            
        # If we have a command, extract the command and parameters (if any)
        if message.content.startswith('!'):
            content =  message.content.split(' ', 1) 
            command = content[0]

            if len(content) > 1:
                parameters = content[1]

        # Go through each of the plugins and see if they can execute the command
        for plugin in self.pluginManager.getPluginsOfCategory("Plugins"):
            # Let the plugin read the message
            if plugin.plugin_object.isReadingMessages():
                plugin.plugin_object.readMessage(message)

            # Check if a plugin can handle the command and execute it if they can
            if command != '' and plugin.plugin_object.checkForCommand(command):
                plugin.plugin_object.executeCommand(command, parameters)

        if 'poop' in message.content:
            fmt = '[Moving user {0.author} to AFK for using a banned word.]'
            check = lambda c: c.name == 'AFK' and c.type == discord.ChannelType.voice

            channel = discord.utils.find(check, message.server.channels)
            await self.move_member(message.author, channel)
            await self.send_message(message.channel, fmt.format(message))

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
            #response = self.cb.ask(question)
            #await self.send_message(message.channel, response)
                
  
styroBot = Bot()
f = open('credentials.txt', 'r')
creds = f.read().splitlines()
email = creds[0]
password = creds[1]
f.close()
styroBot.run(email, password)
