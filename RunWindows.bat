xcopy "%CD%\deps" "%CD%\dist" /e /i /y
xcopy "%CD%\styrobot" "%CD%\dist" /e /i /y
copy "%CD%\credentials.txt" "%CD%\dist\" /y
cd dist && python styrobot.py