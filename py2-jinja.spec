### RPM external py2-jinja 2.5.2
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n Jinja2-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
