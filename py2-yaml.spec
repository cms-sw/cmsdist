### RPM external py2-yaml 3.09
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pyyaml.org/download/pyyaml/PyYAML-%realversion.tar.gz
Requires: python libyaml py2-pyrex

%prep
%setup -n PyYAML-%realversion
cat >> setup.cfg <<-EOF
	[build_ext]
	include_dirs = $LIBYAML_ROOT/include
	library_dirs = $LIBYAML_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py --with-libyaml install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
