#! /usr/bin/bash

# Create log.txt file if it doesn't exist
if [ ! -f log.txt ]; then
	touch log.txt
fi

/usr/bin/python3 -m pip install playwright
/usr/bin/python3 -m playwright install chromium
cp reservation_bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/reservation_bot.plist
