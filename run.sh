#!/bin/bash
# Jal Lijiye - macOS Drinking Water Buddy Launch Script

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ ! -d "venv" ]; then
    echo "Creating virtualenv environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

echo "Starting Jal Lijiye..."
./venv/bin/python main.py
