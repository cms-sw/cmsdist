### RPM external py3-yaml 3.12
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pyyaml.org/download/pyyaml/PyYAML-%realversion.tar.gz
Requires: python3 libyaml py3-pyrex

%prep
%setup -n PyYAML-%realversion
sed -i -e "s,[build_ext],# [build_ext],g" setup.cfg
cat >> setup.cfg <<-EOF
	[build_ext]
	include_dirs = $LIBYAML_ROOT/include
	library_dirs = $LIBYAML_ROOT/lib
EOF

%build
export PYTHON3_ROOT
export LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS"
export LDFLAGS="-L $ZLIB_ROOT/lib $LDFLAGS"
python3 setup.py build

%install
python3 setup.py --with-libyaml install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
