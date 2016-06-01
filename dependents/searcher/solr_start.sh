#!/bin/bash

if [ ! -f "$SEARCHER_SERVICE_CONF" ]; then
  echo "Missing config file solr.conf"
exit 1
fi
. $SEARCHER_SERVICE_CONF

if [ ! -d $SOLR_HOME ]; then
  echo "Can't find $SOLR_HOME"
exit 1
fi

cd $SOLR_WEBAPP_DIR
COMMAND="java $OPTIONS -jar start.jar"
nohup $COMMAND > $LOG_FILE 2>&1 &
echo $! > $PIDFILE
exit $?
