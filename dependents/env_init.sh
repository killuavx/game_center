#!/usr/bin/env bash
#wget -q -O - --no-check-certificate https://github.com/nvie/gitflow/raw/develop/contrib/gitflow-installer.sh | bash
pip-3.3 install virtualenvwrapper
# append your .profile
source /usr/local/bin/virtualenvwrapper.sh
# end

mkvirtualenv --python=python3.3 --no-site-packages GameCenterEnv

pip-3 install Django==1.5.2
(cd django-userena && python3 setup.py install)
(cd django-tagging && python3 setup.py install)
(cd ./django-tagging-autocomplete-0.3.1/ && python3 setup.py install)
(cd easy-thumbnails && python3 setup.py install)
#(cd django_polymorphic && python3 setup.py install)
pip-3 install django-extensions django-model-utils South==0.8.2\
	django-mptt==0.6.0 djangorestframework\
	markdown html2text html5lib\
	pytz django-timezones
pip-3. install six
pip-3. install django-pipeline
pip-3. install -e git+https://github.com/gpolo/pil-py3k#egg=PIL
pip-3. install mysql-python==1.2.4
pip-3.3 install django-autoslug
