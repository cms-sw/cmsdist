### RPM external py2-mysqldb 1.2.3c1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn MySQL-python
Source: http://heanet.dl.sourceforge.net/sourceforge/mysql-python/%downloadn-%realversion.tar.gz
Requires: python mysql 
Patch0: py2-mysqldb-setup

%prep
%setup -n %downloadn-%realversion
%patch0 -p0

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
