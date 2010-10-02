### RPM external py2-pyrex 0.9.9
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
# Source: http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/oldtar/Pyrex-%realversion.tar.gz
Source: http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/Pyrex-%realversion.tar.gz
Requires: python

%prep
%setup -n Pyrex-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
