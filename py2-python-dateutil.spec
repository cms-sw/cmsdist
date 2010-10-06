### RPM external py2-python-dateutil 1.1 
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://labix.org/download/python-dateutil/python-dateutil-%{realversion}.tar.bz2 
Requires: python

%prep
%setup -n python-dateutil-%{realversion} 

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
