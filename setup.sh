#! /usr/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
log_file="$script_dir/log.txt"
plist_file="$script_dir/reservation_bot.plist"

# Create log.txt file if it doesn't exist
if [ ! -f "$log_file" ]; then
	touch "$log_file"
fi

/usr/bin/python3 -m pip install playwright
/usr/bin/python3 -m playwright install chromium
cp "$plist_file" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/reservation_bot.plist
