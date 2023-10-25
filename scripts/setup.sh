#!/bin/sh

scripts_dir=$(dirname "$(readlink -f "$0")")
root_dir=$(dirname "$scripts_dir")
plist_file="$root_dir/reservation_bot.plist"
install_dir="/usr/local/reservation_bot"

# Prompt for the sudo password
sudo -v

# # Check for internet connection
# if ! ping -q -c 2 -W 2 google.com >/dev/null 2>&1; then
# 	printf "There is no internet connection.\n"
# 	printf "Internet connection is needed for running this setup script.\n"
# 	printf "Please, connect to the internet and try again.\n"
# 	exit 1
# fi

# Install the necessary python dependencies
printf "Installing dependencies...\n"
/usr/bin/python3 -m pip install toml >/dev/null
/usr/bin/python3 -m pip install playwright >/dev/null
/usr/bin/python3 -m playwright install chromium >/dev/null

# Get user credentials
printf "\nIntroduce your intranet username and password:\n"
printf "Dni: "
read -r username
printf "Password: "
stty -echo
read -r password
stty echo

printf "\nChecking if the intranet username and password are valid...\n"
credentials_script="$scripts_dir/check_credentials.py"

if ! /usr/bin/python3 "$credentials_script" "$username" "$password"; then
	printf "The intranet username or password are not valid.\n"
	printf "Please, try again.\n"
	exit 1
fi

# Install the script in the system
if [ -d /usr/local/reservation_bot ]; then
	sudo rm -rf "$install_dir"
fi
sudo cp -r "$root_dir/bot" "$install_dir"

# Replace the credentials inside the script
sudo sed -i '' "s/USERNAME = \".*\"/USERNAME = \"$username\"/" "$install_dir/bot.py"
sudo sed -i '' "s/PASSWORD = \".*\"/PASSWORD = \"$password\"/" "$install_dir/bot.py"

# Create the necessary directories and files
if [ ! -d ~/bot_reservas ]; then
	mkdir ~/bot_reservas
fi

if [ ! -f ~/bot_reservas/reservas.toml ]; then
	cp "$root_dir/reservas.toml" ~/bot_reservas/
fi

# Create the launch agent
if [ -f ~/Library/LaunchAgents/reservation_bot.plist ]; then
	launchctl unload ~/Library/LaunchAgents/reservation_bot.plist
fi
sudo cp "$plist_file" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/reservation_bot.plist

printf "\nSetup completed successfully.\n"
