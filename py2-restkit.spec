### RPM external py2-restkit 2.2.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/r/restkit/restkit-2.2.1.tar.gz#md5=ec79eee99e2128763b9b0493a6aa6d9b 
Requires: python py2-setuptools

%prep
%setup -n restkit-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/restcli; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
