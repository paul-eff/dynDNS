#!/bin/bash

# Path to pipenv environment
PIPENV_PATH="/path/to/.local/share/virtualenvs/dynDNS-xxxxxxxx"

# Activate pipenv environment
source "$PIPENV_PATH/bin/activate"

# Run Python script
python3 /patho/to/dynDNS.py

# Deactivate environment
deactivate