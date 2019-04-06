#!/bin/bash

# shellcheck source=/dev/null
SCRIPTPATH=$(dirname "$0")
echo "$SCRIPTPATH"
if ! ping -q -c 1 www.google.com &> /dev/null
then
    echo 'No internet :('
else
    if [ -e "$SCRIPTPATH"'/.env' ]
    then
        source "$SCRIPTPATH"'/.env/bin/activate'
    else
        virtualenv --python=python3.6 "$SCRIPTPATH"'/.env' || exit 2
        source "$SCRIPTPATH"'/.env/bin/activate' || exit 3
        pip install -r "$SCRIPTPATH"'/requirements.txt' --upgrade || exit 4
    fi

    mkdir -p "$SCRIPTPATH"'/tmp'
    python3.6 "$SCRIPTPATH"'/nautilus.py' background.jpg "$1" 31 "${2:-8}" 0.2 "$SCRIPTPATH" || exit 5
    rm -r "$SCRIPTPATH"'/tmp'
    deactivate
    feh --bg-scale "$SCRIPTPATH"'/wallpaper.png'
fi

