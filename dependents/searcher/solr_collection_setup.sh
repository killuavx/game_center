#!/bin/bash
#
if [ ! -f "$SEARCHER_SERVICE_CONF" ]; then
  echo "Missing config file solr.conf"
exit 1
fi
. $SEARCHER_SERVICE_CONF

_CN_NAME=${1:?"Collection Name missing \$1"}

_SCHEMA_CONF=${2:?"schema.xml missing \$2"}

_SOLR_CONF=${3:?"solrconfig.xml missing \$3"}

CN=collection1

CN_DIR=$SOLR_WEBAPP_DIR/solr/$CN

CN_CONF_DIR=$CN_DIR/conf

echo "name=$_CN_NAME" > $CN_DIR/core.properties

rm -rf $CN_CONF_DIR/schema.xml
cp $_SCHEMA_CONF $CN_CONF_DIR/

rm -rf $CN_CONF_DIR/solrconfig.xml
cp $_SOLR_CONF $CN_CONF_DIR/

rm -rf $CN_CONF_DIR/stopwords_en.txt
cp $CN_CONF_DIR/lang/stopwords_en.txt $CN_CONF_DIR/

rm -rf $CN_CONF_DIR/stopwords.txt
cp $CN_CONF_DIR/stopwords_en.txt $CN_CONF_DIR/stopwords.txt
