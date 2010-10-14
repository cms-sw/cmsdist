### RPM external py2-pygments 1.3.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/P/Pygments/Pygments-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n Pygments-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
