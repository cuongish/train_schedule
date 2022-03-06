#!/usr/bin/env bash

if ! command -v pip-compile > /dev/null
then
    echo 'Install pip-tools first! $ python -m pip install pip-tools'
    exit 1
fi

export  CUSTOM_COMPILE_COMMAND='./compile-requirements.sh'

pip-compile --no-header requirements/requirements.in $1 $2 $3
pip-compile --no-header requirements/test-requirements.in $1 $2 $3
