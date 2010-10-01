### RPM external py2-adns 1.2.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn adns-python
Source: http://adns-python.googlecode.com/files/%downloadn-%realversion.tar.gz
Requires: python adns

%prep
%setup -n %downloadn-%realversion
cat >> setup.cfg <<- EOF
	[build_ext]
	include_dirs = $ADNS_ROOT/include
	library_dirs = $ADNS_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
