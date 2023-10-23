#!/bin/sh

scripts_dir=$(dirname "$(readlink -f "$0")")

# Check for internet connection
if ! ping -q -c 2 -W 2 google.com >/dev/null 2>&1; then
	printf "There is no internet connection.\n"
	printf "Internet connection is needed for running this setup script.\n"
	printf "Please, connect to the internet and try again.\n"
	exit 1
fi

# Check for Python3
if ! command -v /usr/bin/python3 2>&1; then
	printf "Python is not installed.\n"
	printf "Please, check your python installation and try again\n"
	exit 1
fi

/usr/bin/python3 "$scripts_dir/setup.py"

# Replace the credentials in the script
# Create the necessary directories and files
# Create the launch agent

# root_dir=$(dirname "$scripts_dir")
# plist_file="$root_dir/reservation_bot.plist"
