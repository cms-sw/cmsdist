### RPM external py2-elasticsearch 2.3.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/elastic/elasticsearch-py.git?obj=master/%{realversion}&export=ElasticSearch-%{realversion}&output=/ElasticSearch-%{realversion}.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n ElasticSearch-%realversion

%build
python setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
find %i/$PYTHON_LIB_SITE_PACKAGES -name '*.py' -exec chmod a-x {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
