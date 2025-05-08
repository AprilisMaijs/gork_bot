#!/bin/bash
# Start the keep-alive server in the background
python3 keep_alive.py &

# Start the bot
python3 main.py
