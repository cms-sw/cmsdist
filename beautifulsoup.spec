### RPM external beautifulsoup 3.1.0.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://www.crummy.com/software/BeautifulSoup/download/3.1.x/BeautifulSoup-%{realversion}.tar.gz
Requires: python

%prep
%setup -n BeautifulSoup-%{realversion}

%build
python setup.py build 

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

