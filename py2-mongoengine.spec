### RPM external py2-mongoengine 0.3
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://github.com/hmarr/mongoengine/tarball/v0.3
Requires: python py2-sphinx py2-setuptools

%prep
%setup -n hmarr-mongoengine-*

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

