### RPM external py2-future 0.15.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/f/future/future-%realversion.tar.gz
Requires: python py2-setuptools py2-importlib

%prep
%setup -n future-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null

# Don't delete egg-info since the futurize script need it to load the future library
#find %i -name '*.egg-info' -print0 | xargs -0 rm -rf --

# Fix hardcoded path to python
egrep -r -l '^#!.*python' %i/bin | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
