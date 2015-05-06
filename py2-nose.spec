### RPM external py2-nose 1.3.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pypi.python.org/packages/source/n/nose/nose-%{realversion}.tar.gz
Requires: python

%prep
%setup -n nose-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
