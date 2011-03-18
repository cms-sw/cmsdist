### RPM external mechanize 0.2.4
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://wwwsearch.sourceforge.net/mechanize/src/mechanize-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n mechanize-%realversion
%build
python setup.py build
%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -print0 | xargs -0 rm -rf
