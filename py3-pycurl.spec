### RPM external py3-pycurl 7.19.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pycurl.sourceforge.net/download/pycurl-%realversion.tar.gz
Requires: openssl python3 curl

%prep
%setup -n pycurl-%realversion
perl -p -i -e 's/,\s+"--static-libs"]/]/' setup.py

%build
export CPPFLAGS="-I ${OPENSSL_ROOT}/include $CPPFLAGS"
export PYTHON3_ROOT
export LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS"
python3 setup.py build --with-ssl

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
# replace all instances of #!/path/bin/python into proper format
for f in `find %i -type f`; do
    if [ -f $f ]; then
        perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python.*}' $f
    fi
done

# Remove documentation.
%define drop_files %i/share

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
