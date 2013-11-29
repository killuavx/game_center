#!/bin/bash
if [ ! -f "$SEARCHER_SERVICE_CONF" ]; then
  echo "Missing config file solr.conf"
exit 1
fi
. $SEARCHER_SERVICE_CONF

DL_URL="http://mirror.esocc.com/apache/lucene/solr/4.6.0/solr-4.6.0.tgz"

DL_NAME=`basename $DL_URL`

DIR_NAME=${DL_NAME%.*}

SOLR_DIR=$DIR_NAME

function solr_download()
{
  curl -o $DL_NAME $DL_URL
  tar zxvf $DL_NAME
}

function solr_install()
{
  rm -rf $SOLR_HOME
  ln -s $SOLR_DIR $SOLR_HOME
}

solr_download && solr_install
