#! /usr/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
plist_file="$script_dir/reservation_bot.plist"

if [ ! -d ~/bot_reservas ]; then
	mkdir ~/bot_reservas
fi

if [ ! -f ~/bot_reservas/reservas.toml ]; then
	cp "$script_dir/reservas.toml" ~/bot_reservas/ || touch ~/bot_reservas/reservas.toml
fi

if [ ! -d /usr/local/reservation_bot ]; then
	sudo cp -r "$script_dir/bot" /usr/local/reservation_bot
fi

/usr/bin/python3 -m pip install playwright
/usr/bin/python3 -m playwright install chromium

# if there is a previous version of the plist file, unload it
if [ -f ~/Library/LaunchAgents/reservation_bot.plist ]; then
	launchctl unload ~/Library/LaunchAgents/reservation_bot.plist
fi

cp "$plist_file" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/reservation_bot.plist
