pyinstaller --onefile -p "%CD%\styrobot" "%CD%\styrbot\styrobot.py"
xcopy "%CD%\deps" "%CD%\dist" /E 
xcopy "%CD%\styrobot\plugins" "%CD%\dist\plugins" /E
