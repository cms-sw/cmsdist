### RPM external py2-mako 0.3.6
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn Mako
Source: http://www.makotemplates.org/downloads/%downloadn-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n %downloadn-%realversion

%build
python setup.py build

%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
PYTHONPATH=${PYTHONPATH}:%i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
