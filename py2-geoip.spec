### RPM external py2-geoip 1.2.4
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn GeoIP-Python
Source: http://geolite.maxmind.com/download/geoip/api/python/%downloadn-%realversion.tar.gz
Requires: python geoip

%prep
%setup -n %downloadn-%realversion
cat >> setup.cfg <<- EOF
	[build_ext]
	include_dirs = $GEOIP_ROOT/include
	library_dirs = $GEOIP_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
