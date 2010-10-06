### RPM external py2-cheetah 2.4.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://pypi.python.org/packages/source/C/Cheetah/Cheetah-%realversion.tar.gz
Requires: python

%prep
%setup -n Cheetah-%realversion
%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
