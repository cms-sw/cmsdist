### RPM external py2-coverage 3.5.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://bitbucket.org/ned/coveragepy/get/coverage-%{realversion}.tar.gz
Requires: python py2-setuptools

%prep
%setup -n ned-coveragepy-465bedd8af1f

%build
python setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
find %i/$PYTHON_LIB_SITE_PACKAGES -name '*.py' -exec chmod a-x {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
