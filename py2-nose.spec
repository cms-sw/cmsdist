### RPM external py2-nose 1.1.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://bitbucket.org/jpellerin/nose/get/af3d9e0d2299.tar.bz2
#Source: http://pypi.python.org/packages/source/n/nose/nose-%{realversion}.tar.gz
Requires: python

%prep
%setup -n jpellerin-nose-af3d9e0d2299

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
