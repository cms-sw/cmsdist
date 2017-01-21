### RPM external py3-scons 2.5.1
## INITENV +PATH PYTHONPATH %i/lib/%n-%realversion
Source: http://prdownloads.sourceforge.net/scons/scons-%realversion.tar.gz
Requires: python3

%prep
%setup -n scons-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
%define drop_files %i/man
