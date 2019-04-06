#!/bin/bash

SCRIPTPATH=$(dirname "$SCRIPT")
find "$SCRIPTPATH" -name 'wallpaper.png' -mmin +31 -exec sh -c "$SCRIPTPATH'/wallpaper.sh' MiEI" \;
