#!/usr/bin/env bash

# Checks if Python is installed
if ! command -v python3 &>/dev/null
then
    echo "Python 3 is not installed, please install Python first..."
    exit 1
fi

# Creates the Linux virtual environment if not exists
if ! [ -d venv_linux ]
then
    echo "Creating the Linux virtual environment..."
    python3 -m venv venv_linux
fi

# Prepares the virtual environment
. venv_linux/bin/activate
pip install --upgrade pip
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d'=' -f 1 | xargs -n1 pip install -U
pip install -r requirements.txt
