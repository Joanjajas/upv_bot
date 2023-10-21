#! /usr/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
plist_file="$script_dir/reservation_bot.plist"
install_dir="/usr/local/reservation_bot"

# Check internet connection
if ! ping -q -c 2 -W 2 google.com >/dev/null 2>&1; then
	printf "No hay conexión a internet.\n"
	printf "Se necesita conexión a internet para el proceso de setup.\n"
	printf "Por favor, conectate a internet e inténtalo de nuevo.\n"
	exit 1
fi

# Ask for sudo permissions
sudo -v

# Install the necessary python dependencies
printf "\nInstalando dependencias...\n"
/usr/bin/python3 -m pip install playwright >/dev/null
/usr/bin/python3 -m playwright install chromium >/dev/null

# Get user credentials
while true; do
	printf "Introduce el usuario y contraseña de la intranet.\n"
	read -r -p "DNI: " username
	read -r -s -p "Contraseña: " password

	printf "\nComprobando que el usuario y la contraseña son correctos...\n"

	credentials_script="$script_dir/check_credentials.py"

	# Check that the credentials are correct
	if /usr/bin/python3 "$credentials_script" "$username" "$password"; then
		break
	else
		printf "El usuario o la contraseña son incorrectos.\n\n"
	fi
done

# Copy the bot script to the correct directory
if [ -d /usr/local/reservation_bot ]; then
	sudo rm -rf /usr/local/reservation_bot
fi
sudo cp -r "$script_dir/bot" /usr/local/reservation_bot/

# Replace the credentials in the script
sudo sed -i '' "s/USERNAME = \".*\"/USERNAME = \"$username\"/" "$install_dir/bot.py"
sudo sed -i '' "s/PASSWORD = \".*\"/PASSWORD = \"$password\"/" "$install_dir/bot.py"

# Make sure to create the necessary directories and files
if [ ! -d ~/bot_reservas ]; then
	mkdir ~/bot_reservas
fi

if [ ! -f ~/bot_reservas/reservas.toml ]; then
	cp "$script_dir/reservas.toml" ~/bot_reservas/
fi

# Create the launch agent
if [ -f ~/Library/LaunchAgents/reservation_bot.plist ]; then
	launchctl unload ~/Library/LaunchAgents/reservation_bot.plist
fi

cp "$plist_file" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/reservation_bot.plist
