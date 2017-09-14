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
# replace all instances of #!/path/bin/python into proper format
for f in `find %i -type f`; do
    if [ -f $f ]; then
        perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python.*}' $f
    fi
done

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
