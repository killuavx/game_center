#!/usr/bin/env bash
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
python3.3 ez_setup.py
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python3.3 get-pip.py

pip-3.3 install virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.3
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv --python=`which python3.3` --no-site-packages GameCenterEnv
