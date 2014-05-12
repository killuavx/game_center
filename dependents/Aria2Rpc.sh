#!/bin/sh
RUNTIME_DIR=/tmp/aria2/
TMP_DIR=/tmp/aria2/
SESSION_FILE=${RUNTIME_DIR}aria2.session
mkdir -p $TMP_DIR
touch $SESSION_FILE
PREFIX=/opt/local/bin/
${PREFIX}aria2c --event-poll=select --dir=$TMP_DIR -s 5 --enable-rpc --rpc-listen-all=true --rpc-allow-origin-all -c -D --save-session=$SESSION_FILE --input-file=$SESSION_FILE

# sudo chmod +x /etc/init.d/Aria2.sh
# sudo update-rc.d /etc/init.d/Aria2.sh defaults
