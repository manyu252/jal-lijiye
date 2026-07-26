#!/usr/bin/env bash
# Double-clickable macOS launcher for Jal Lijiye
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ -d "dist/Jal Lijiye.app" ]; then
    open "dist/Jal Lijiye.app"
else
    ./run.sh
fi
