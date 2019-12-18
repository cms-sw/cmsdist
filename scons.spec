### RPM external scons 3.0.1
## INITENV +PATH PYTHONPATH %i/lib/%n-%realversion
Source: http://prdownloads.sourceforge.net/scons/scons-%realversion.tar.gz
Requires: python

%prep
%setup -n scons-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
