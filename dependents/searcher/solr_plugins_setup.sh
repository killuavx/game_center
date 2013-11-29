#!/bin/bash
#
if [ ! -f "$SEARCHER_SERVICE_CONF" ]; then
  echo "Missing config file solr.conf"
exit 1
fi

. $SEARCHER_SERVICE_CONF
IK_JAR=$SEARCHER_SCRIPT_DIR/plugins/IKAnalyzer2012FF_u1.jar
cp $IK_JAR $SOLR_WEBAPP_DIR/resources/
