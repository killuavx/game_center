#!/usr/bin/env bash
pip-3.3 install virtualenvwrapper
# append your .profile
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
# end


mkvirtualenv --python=python3.3 --no-site-packages GameCenterEnv
