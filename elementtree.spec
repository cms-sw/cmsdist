### RPM external elementtree 1.2.6
## INITENV +PATH PYTHONPATH %i/share/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://effbot.org/downloads/%n-%realversion-20050316.zip
Requires: python
 
%prep
%setup -n %n-%realversion-20050316

%build
python setup.py build

%install
python setup.py install --prefix=%i/share
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
