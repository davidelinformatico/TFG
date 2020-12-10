#!/bin/bash

if ps | grep bot; then
    echo "todo bien"
else
    cd /home/pi/source/TFG/scripts/bot/
    python3 /home/pi/source/TFG/scripts/bot/bot.py
fi

