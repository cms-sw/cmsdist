### RPM external py2-restkit 2.2.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/r/restkit/restkit-2.2.1.tar.gz#md5=ec79eee99e2128763b9b0493a6aa6d9b 
Requires: python py2-setuptools

%prep
%setup -n restkit-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

