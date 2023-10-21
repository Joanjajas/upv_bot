#!/bin/sh

script_dir=$(dirname "$(readlink -f "$0")")
plist_file="$script_dir/reservation_bot.plist"
install_dir="/usr/local/reservation_bot"

main() {
	install_deps
	get_credentials
	check_credentials
	install_script
	replace_credentials
	create_dirs
	create_launch_agent
}

# Install the necessary python dependencies
install_deps() {
	printf "\nInstalling dependencies...\n"
	/usr/bin/python3 -m pip install playwright >/dev/null
	/usr/bin/python3 -m playwright install chromium >/dev/null
}

# Prompt for username and password
get_credentials() {
	printf "Introduce your intranet username and password:\n"
	printf "Dni: "
	read -r username
	printf "Password: "
	stty -echo
	read -r password
	stty echo
}

# Check that the credentials are correct
check_credentials() {
	while true; do
		printf "\nChecking if the intranet username and password are valid...\n"

		credentials_script="$script_dir/check_credentials.py"

		if /usr/bin/python3 "$credentials_script" "$username" "$password"; then
			break
		else
			printf "The intranet username or password are not valid.\n\n"
			get_credentials
		fi
	done
}

# Install the script in the system
install_script() {
	if [ -d /usr/local/reservation_bot ]; then
		sudo rm -rf "$install_dir"
	fi
	sudo cp -r "$script_dir/bot" "$install_dir"
}

# Replace the credentials in the script
replace_credentials() {
	sudo sed -i '' "s/USERNAME = \".*\"/USERNAME = \"$username\"/" "$install_dir/bot.py"
	sudo sed -i '' "s/PASSWORD = \".*\"/PASSWORD = \"$password\"/" "$install_dir/bot.py"
}

# Create the necessary directories and files
create_dirs() {
	if [ ! -d ~/bot_reservas ]; then
		mkdir ~/bot_reservas
	fi

	if [ ! -f ~/bot_reservas/reservas.toml ]; then
		cp "$script_dir/reservas.toml" ~/bot_reservas/
	fi
}

# Create the launch agent
create_launch_agent() {
	if [ -f ~/Library/LaunchAgents/reservation_bot.plist ]; then
		launchctl unload ~/Library/LaunchAgents/reservation_bot.plist
	fi

	sudo cp "$plist_file" ~/Library/LaunchAgents/
	launchctl load ~/Library/LaunchAgents/reservation_bot.plist
}

# Prompt for the sudo password
sudo -v

# Check for internet connection
if ! ping -q -c 2 -W 2 google.com >/dev/null 2>&1; then
	printf "There is no internet connection.\n"
	printf "Internet connection is needed for running this setup script.\n"
	printf "Please, connect to the internet and try again.\n"
	exit 1
fi

main
