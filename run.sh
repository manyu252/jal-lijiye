#!/bin/bash
# Jal Lijiye - macOS Drinking Water Buddy Launch Script

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ ! -d "venv" ]; then
    echo "Creating virtualenv environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

if [ -f "walki_in_video.mp4" ] || [ -f "walk_in_video.mp4" ]; then
    echo "Processing video files (walk_in & walk_out)..."
    ./venv/bin/python scripts/process_new_videos.py
elif [ -f "walk_video.mp4" ]; then
    echo "Processing walk_video.mp4..."
    ./venv/bin/python scripts/convert_video_to_gif.py
elif [ -f "my_character.png" ]; then
    echo "Processing custom character from my_character.png..."
    ./venv/bin/python scripts/process_user_character.py
elif [ ! -f "assets/icon.png" ]; then
    echo "Generating default pixel assets..."
    ./venv/bin/python scripts/generate_assets.py
fi

echo "Starting Jal Lijiye..."
./venv/bin/python main.py
