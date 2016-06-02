#!/bin/bash
command -v pip >/dev/null 2>&1 || {
echo >&2 "This script requires pip but it's not installed. Please install pip before running this script. Aborting.";
exit 1;
}
input=''
echo "Would you like to update pip first? (y/n): "
read -n 1 input
echo

if [ "$input" = "y" ] || [ "$input" = "Y" ]; then
    pip install --upgrade pip
fi

echo "Installing Dependencies for StyroBotPy"

echo "Installing Discord.py"
pip install git+https://github.com/Rapptz/discord.py@async
echo "Complete!"
echo "Installing Cleverbot"
pip install cleverbot
echo "Complete!"
echo "Installing Youtube-dl"
pip install youtube-dl 
echo "Complete!"
echo "Installing Pafy"
pip install pafy
echo "Complete!"
echo "Installing Yapsy"
pip install yapsy
echo "Complete!"
echo "All Dependencies have been Installed!"
