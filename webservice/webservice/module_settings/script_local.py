# -*- coding: utf-8 -*-
import os

# for use nvm node
os.environ['PATH'] = "%s:%s" % ('/Users/me/.nvm/v0.11.9/bin', os.environ['PATH'])
AAPT_CMD = '/Applications/adt-bundle-mac-x86_64/sdk/platform-tools/aapt'
# for solr
os.environ['SOLR_HOME'] = SOLR_HOME = '/var/lib/solr'

#Path to CoffeeScript compiler executable
COFFEESCRIPT_EXECUTABLE = \
    '/Users/me/.nvm/v0.11.9/lib/node_modules/coffee-script/bin/coffee'

#Path to less script compiler executable
LESS_EXECUTABLE = '/Users/me/.nvm/v0.11.9/bin/lessc'
