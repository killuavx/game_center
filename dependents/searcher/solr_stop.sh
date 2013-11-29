#!/bin/bash

if [ ! -f "$SEARCHER_SERVICE_CONF" ]; then
  echo "Missing config file solr.conf"
exit 1
fi
. $SEARCHER_SERVICE_CONF

kill -9 `cat $PIDFILE`

rm -rf $PIDFILE
