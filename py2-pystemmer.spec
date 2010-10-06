### RPM external py2-pystemmer 1.0.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://snowball.tartarus.org/wrappers/PyStemmer-%{realversion}.tar.gz
Requires: python 

%prep
%setup -n PyStemmer-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

