#!/usr/bin/env bash
(cd ../webservice && pip-3.3 install -r requirements.txt)
(cd ../webservice && pip-3.3 install -r requirements-dev.txt)
(cd django-userena && python3 setup.py install)
(cd django-tagging && python3 setup.py install)
(cd django-tagging-autocomplete-0.3.1/ && python3 setup.py install)
(cd easy-thumbnails && python3 setup.py install)
#(cd django_polymorphic && python3 setup.py install)
