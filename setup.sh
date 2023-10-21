#! /usr/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
plist_file="$script_dir/reservation_bot.plist"

# Install the necessary python dependencies
/usr/bin/python3 -m pip install playwright
/usr/bin/python3 -m playwright install chromium

# Get user credentials
while true; do
	printf "\nIntroduce el usuario y contraseña de la intranet.\n"
	read -r -p "DNI: " username
	read -r -s -p "Contraseña: " password

	credentials_script="$script_dir/check_credentials.py"

	printf "\nComprobando que el usuario y la contraseña son correctos...\n"

	if /usr/bin/python3 "$credentials_script" "$username" "$password"; then
		break
	else
		printf "El usuario o la contraseña son incorrectos.\n"
	fi
done

sed -i '' "s/USERNAME = \".*\"/USERNAME = \"$username\"/" "$script_dir/bot/bot.py"
sed -i '' "s/PASSWORD = \".*\"/PASSWORD = \"$password\"/" "$script_dir/bot/bot.py"

# Make sure to create the necessary directories and files
if [ ! -d ~/bot_reservas ]; then
	mkdir ~/bot_reservas
fi

if [ ! -f ~/bot_reservas/reservas.toml ]; then
	cp "$script_dir/reservas.toml" ~/bot_reservas/
fi

if [ ! -d /usr/local/reservation_bot ]; then
	sudo cp -r "$script_dir/bot" /usr/local/reservation_bot
fi

# Create the launch agent
if [ -f ~/Library/LaunchAgents/reservation_bot.plist ]; then
	launchctl unload ~/Library/LaunchAgents/reservation_bot.plist
fi

cp "$plist_file" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/reservation_bot.plist
