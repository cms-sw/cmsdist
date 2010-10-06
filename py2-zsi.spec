### RPM external py2-zsi 2.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

Source: http://switch.dl.sourceforge.net/sourceforge/pywebsvcs/ZSI-%{realversion}.tar.gz
Requires: python py2-pyxml

%prep 
%setup -n ZSI-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
