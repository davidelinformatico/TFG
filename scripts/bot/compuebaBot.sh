#!/bin/bash
path=$(pwd)

if ps | grep bot; then
    echo "todo bien"
else
    python3 bot.py
fi

