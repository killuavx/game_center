#!/usr/bin/env bash
pip-3.3 install virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.3
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv --python=python3.3 --no-site-packages GameCenterEnv
