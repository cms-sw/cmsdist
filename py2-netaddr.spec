### RPM external py2-netaddr 0.7.4
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://download.github.com/drkjam-netaddr-rel-0.7.4-0-g2a22077.tar.gz
Requires: python

%prep
%setup -n drkjam-netaddr-3d45e61

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
