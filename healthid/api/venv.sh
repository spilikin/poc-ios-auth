#!/bin/bash
if [ ! -f ./requirements.txt ] 
    then
        echo "ERROR: requirements.txt not found"
        return
fi
if [ ! -f ./.virtualenv/bin/activate ]
    then
        pip install virtualenv 2> /dev/null
        python3 -m virtualenv --python=python3.7 ./.virtualenv
fi
echo Activating virtualenv
source ./.virtualenv/bin/activate
pip install -r ./requirements.txt
