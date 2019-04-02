SCRIPTPATH=$(dirname "$SCRIPT")
find ./ -name 'wallpaper.png' -mmin +31 -exec $SCRIPTPATH'/wallpaper.sh' \;
