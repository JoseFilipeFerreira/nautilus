#!/bin/bash
if [ -e .env ]
then
    source .env/bin/activate
else
    virtualenv --python=python3.6 .env
    source .env/bin/activate
    pip install -r requirements.txt --upgrade
fi

python3.6 nautilus.py background.jpg LEO 31 8 0.2
rm tmp/*
deactivate