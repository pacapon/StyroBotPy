# StyroBotPy
Python version of my custom DiscordBot, based on Rapptz discord.py

# Requirements
- Python 3.5
- discord.py
- cleverbot.py
- pafy
- yapsy

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
4. pip install yapsy
5. In order to properly run audio stuff, you need have ffmpeg in your PATH variable. 

## Creating an Executable
### Option 1: Automatically
**WINDOWS**

1. Run "CreateExecutable.bat"

**LINUX**

1. Run "make"

### Option 2: Manually with PyInstaller
**WINDOWS & LINUX**

1. Install Python 3.5
2. Open a cmd window in your project folder
3. Run "pip install pyinstaller"
4. Run "pyinstaller --onefile -p ./styrobot/ ./styrobot/styrobot.py -n styrobotpy"
5. Make sure you include a "music/" and "images/" folder, as well as opus.dll and credentials.txt in the folder with the EXE (which should be called dist by default)

### Option 3: Manually with Python
**WINDOWS & LINUX**

1. Install Python 3.5
2. Open a cmd window in the styrobot directory of your project folder
3. Run "python -m styrobot.py"
4. Make sure you include a "music/" and "images/" folder, as well as opus.dll and credentials.txt in the folder where styrobot.py is

## Bot Commands
Type "!help" in the chat to see a list of all the commands the bot supports as well as all the commands the plugins support!
