### RPM external py2-geoip 1.2.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
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
find %i -name '*.egg-info' -exec rm {} \;
