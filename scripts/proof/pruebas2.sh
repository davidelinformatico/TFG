#!/bin/bash
path=$(pwd)
comp=$(ps | grep bot | wc -l)

if [comp < 1]; then
    python3 ${path%/*}/bot.py











