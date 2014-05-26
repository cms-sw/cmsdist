### RPM external py2-adns 1.2.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
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
find %i -name '*.egg-info' -exec rm {} \;
