#!/bin/bash
# USAGE: wallup [/--no-update]
cd $(dirname "$(readlink -f "$0")")

IMAGE="background.jpg"
SERVER="MiEI"

[ -f 'wallpaper.png' ] && feh --no-fehbg --bg-scale 'wallpaper.png'
[ "$1" = "--no-update" ] && exit 2

if ! ping -q -c 1 www.google.com &> /dev/null
then
    echo 'No internet :('
else
    if [ -e '.env' ]
    then
        source '.env/bin/activate'
    else
        virtualenv '.env' || exit 3
        source '.env/bin/activate' || exit 4
        pip install -r 'requirements.txt' --upgrade || exit 5
    fi

    mkdir -p 'tmp'
    width=$(identify -format "%w" "$IMAGE")> /dev/null
    python 'nautilus.py' "$SERVER" 31 "$width" || exit 6

    ww=$(convert "$IMAGE" -format "%[fx:0.22*w]" info:)
    magick $IMAGE \( foreground.png -resize ${ww}x \) -gravity NorthEast -composite wallpaper.png

    rm -r 'tmp'
    deactivate
    feh --no-fehbg --bg-scale 'wallpaper.png'
fi

