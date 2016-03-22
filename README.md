# StyroBotPy
Python version of my custom DiscordBot, based on Rapptz discord.py

## DEPENDENCIES:
### Option 1: Automatically 
#### WINDOWS
1. Run "InstallDependencies.bat"

#### LINUX
1. Run "InstallDependencies.sh" OR "make install"

### Option 2: Manually 
#### WINDOWS & LINUX
1. pip install git+https://github.com/Rapptz/discord.py@async
2. pip install cleverbot
3. pip install pafy
4. In order to properly run audio stuff, you need have ffmpeg in your PATH variable. 

## CREATING AN EXECUTABLE:
### Option 1: Automatically
#### WINDOWS
1. Run "CreateExecutable.bat"

#### LINUX
1. Run "make"

### Option 2: Manually
#### WINDOWS & LINUX
1. Install Python 3.5
2. Open a cmd window in your project folder
3. Run "pip install pyinstaller"
4. Run "pyinstaller --onefile StyroBotPy.py"
5. Make sure you include a "music/" and "images/" folder, as well as opus.dll and credentials.txt in the folder with the EXE.
