#!/bin/bash
command -v pip >/dev/null 2>&1 || {
echo >&2 "This script requires pip but it's not installed. Please install pip before running this script. Aborting.";
exit 1;
}
echo "Would you like to update pip first? (y/n): "

echo "Installing Dependencies for StyroBotPy"

echo "Installing Discord.py"
pip install git+https://github.com/Rapptz/discord.py@async
echo "Complete!"
echo "Installing Cleverbot"
pip install cleverbot
echo "Complete!"
echo "Installing Pafy"
pip install pafy
echo "Complete!"
echo "All Dependencies have been Installed!"
