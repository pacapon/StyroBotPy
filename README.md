# StyroBotPy
Python version of my custom DiscordBot, based on Rapptz discord.py

## Installing Dependencies
### Option 1: Automatically 
**WINDOWS**

1. Run "InstallDependencies.bat"

**LINUX**

1. Run "InstallDependencies.sh" OR "make install"

### Option 2: Manually 
**WINDOWS & LINUX**

1. pip install git+https://github.com/Rapptz/discord.py@async
2. pip install cleverbot
3. pip install pafy
4. In order to properly run audio stuff, you need have ffmpeg in your PATH variable. 

## Creating an Executable
### Option 1: Automatically
**WINDOWS**

1. Run "CreateExecutable.bat"

**LINUX**

1. Run "make"

### Option 2: Manually
**WINDOWS & LINUX**

1. Install Python 3.5
2. Open a cmd window in your project folder
3. Run "pip install pyinstaller"
4. Run "pyinstaller --onefile StyroBotPy.py"
5. Make sure you include a "music/" and "images/" folder, as well as opus.dll and credentials.txt in the folder with the EXE.

## Bot Commands
Command | Description
--- | ---
!help | Prints out the commands available
!hello | Say Hello
!joinvoice <name> | Join voice channel <name>
!leave | Leave the current voice channel
!pause | Pause the currently playing song
!resume | Resume the currently paused song
!next <songname> | Queue the song to be played next
!play | Play the queued songs
!addsong <url> <name> | Download song at <url> for playback using <name>
!addnq <url> <name> | Download song at <url> for playback using <name> and queue
!skip | Skip the currently playing song
!chat <message> | Send a message to cleverbot
!f14 | Create an F14!
!changebotname <name> | Change the name of the bot to <name>
!shutdown | Shutdown the bot


