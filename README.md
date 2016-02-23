# StyroBotPy
Python version of my custom DiscordBot, based on Rapptz discord.py

** DEPENDENCIES **
1. pip install git+https://github.com/Rapptz/discord.py@async
2. pip install cleverbot.py
3. In order to properly run audio stuff, you need have ffmpeg in your PATH variable.

** CREATING AN EXECUTABLE **
1. Install Python 3.5
2. Open a cmd window in your project folder
3. Run "pip install pyinstaller"
4. Run "pyinstaller --onefile StyroBotPy.py"
5. Make sure you include a "music/" and "images/" folder, as well as opus.dll and credentials.txt in the folder with the EXE.
