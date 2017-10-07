# StyroBotPy
An extendable, plugin driven, discord bot framework based on Rapptz discord.py

## Requirements
- Python 3.5
- discord.py
- cleverbot.py
- pafy
- youtube-dl
- yapsy
- ffmpeg (if you want to use audio stuff)

## Installing Dependencies
### Option 1: Automatically 
**WINDOWS**

1. Run "InstallDependencies.bat"
2. Download ffmpeg and make sure its in your PATH variable

**LINUX**

1. Run "InstallDependencies.sh" OR "make install"
2. Download ffmpeg with your favorite package manager

### Option 2: Manually 
**WINDOWS & LINUX**

1. pip install -U discord.py[voice]
2. pip install cleverbot
3. pip install pafy
4. pip install yapsy
5. Download ffmpeg and make sure its in your PATH variable

## Running with Python
**WINDOWS**
1. Make sure Python 3.5 is installed and you have all necessary dependencies (see above section for more details).
2. Run "RunWindows.bat" 

Note: You will need to either replace the credentials.txt file in the /deps directory or have one in the root directory (the same location as RunWindows.bat). The bat file should automatically copy it to the /dist directory for you. If your credentials file is not properly setup, the bot won't login or work.

**LINUX**

1. Make sure Python 3.5 is installed and you have all necessary dependencies (see above section for more details).
2. Open a cmd window in the styrobot directory of your project folder
3. Run "make copy" (first time only, see note)
4. Run "make runpy" / "make rerun" (See note)

Note: The first time you run the bot, you need to run copy. This will make sure the code and dependencies are in the /dist directory. Afterwards, it should only be necssary to run "make rerun" if you've updated the code or "make runpy" if nothing has changed.

## Bot Commands
Type "!help" in the chat to see a list of all the commands the bot supports as well as all the commands the plugins support!

## Setting up your credentials file
The bot has been setup to use a file, credentials.txt, to login. This file has to be added by the user as they will obviously have their own credentials for their bot (see below on how to add a bot to a server). The credentials file is setup with two lines. The first being the application id and the second being the authentication token used to login. If you want to simplify this a little, feel free to modify the flow in styrobot.py (bottom of the file)! Your file will probably look something like this:
```
891234943217123478
ASDjkwq.jxASDfjioeqwkl.dasdASDFKJdj.2jKOLAs90ASDFjk2l1.kDEF
```

## Adding a Bot to a Server
Once you've created your application and bot under your discord account, you can add that bot to a server. To do so, just paste this url into your browser, changing ### to whatever your application's id is. It will be the long number under App Details called "Client/Application ID".  
```
https://discordapp.com/oauth2/authorize?client_id=###&scope=bot&permissions=0
```

For more info, check out the official documentation here: https://discordapp.com/developers/docs/topics/oauth2
