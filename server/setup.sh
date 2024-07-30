#!/bin/bash

# Define the file path
FILE="./.server_env"

# Check if the file exists
if [ -e "$FILE" ]; then
	source "./.server_env/bin/activate"
else
	python3 -m venv .server_env
	source "./.server_env/bin/activate"
fi

pip install -r requirements.txt

sudo fastapi dev main.py
