#!/bin/bash

SCRIPTPATH=$(dirname "$0")
IMAGE="$SCRIPTPATH/background.jpg"

echo "$SCRIPTPATH"
if ! ping -q -c 1 www.google.com &> /dev/null
then
    echo 'No internet :('
else
    feh --no-fehbg --bg-scale "$SCRIPTPATH"'/wallpaper.png'
    if [ -e "$SCRIPTPATH"'/.env' ]
    then
        source "$SCRIPTPATH"'/.env/bin/activate'
    else
        virtualenv "$SCRIPTPATH"'/.env' || exit 2
        source "$SCRIPTPATH"'/.env/bin/activate' || exit 3
        pip install -r "$SCRIPTPATH"'/requirements.txt' --upgrade || exit 4
    fi

    mkdir -p "$SCRIPTPATH"'/tmp'
    width=$(identify -format "%w" "$IMAGE")> /dev/null
    python "$SCRIPTPATH"'/nautilus.py' "$1" 31 "$width" || exit 5

    ww=$(convert "$IMAGE" -format "%[fx:0.22*w]" info:)
    magick $IMAGE \( "$SCRIPTPATH"/foreground.png -resize ${ww}x \) -gravity NorthEast -composite "$SCRIPTPATH"/wallpaper.png

    rm -r "$SCRIPTPATH"'/tmp'
    deactivate
    feh --no-fehbg --bg-scale "$SCRIPTPATH"'/wallpaper.png'
fi

