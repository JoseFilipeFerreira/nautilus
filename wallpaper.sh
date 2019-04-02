#!/bin/bash
SCRIPTPATH=$(dirname $0)
echo $SCRIPTPATH
if [ ping -q -c 1 www.google.com &> /dev/null ]
then
    echo 'No internet :('
else
    if [ -e $SCRIPTPATH'/.env' ]
    then
        source $SCRIPTPATH'/.env/bin/activate'
    else
        virtualenv --python=python3.6 $SCRIPTPATH'/.env'
        source $SCRIPTPATH'/.env/bin/activate'
        pip install -r $SCRIPTPATH'/requirements.txt' --upgrade
    fi

    mkdir $SCRIPTPATH'/tmp'
    python3.6 $SCRIPTPATH'/nautilus.py' background.jpg MiEI 31 8 0.2 $SCRIPTPATH
    rm -r $SCRIPTPATH'/tmp'
    deactivate
    feh --bg-scale $SCRIPTPATH'/wallpaper.png'
fi

