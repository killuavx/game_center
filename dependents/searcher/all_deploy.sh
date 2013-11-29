export SEARCHER_SERVICE_CONF=`pwd`/solr.conf
export SEARCHER_SCRIPT_DIR=`pwd`
export SOLR_HOME=`pwd`/solr

. $SEARCHER_SCRIPT_DIR/solr_deploy.sh
. $SEARCHER_SCRIPT_DIR/solr_plugins_setup.sh
. $SEARCHER_SCRIPT_DIR/solr_collection_setup.sh package \
  $SEARCHER_SCRIPT_DIR/collection_package_conf/schema.xml \
  $SEARCHER_SCRIPT_DIR/collection_package_conf/solrconfig.xml

