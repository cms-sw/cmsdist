### RPM external apache24-mod_gridsite 2_3_4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
#Source0: https://github.com/CESNET/gridsite/archive/%realversion.tar.gz
Source0: https://github.com/CESNET/gridsite/archive/gridsite-core_R_%realversion.zip
Requires: apache24 python libtool doxygen openssl libxml2

%prep
%setup -n gridsite-gridsite-core_R_%realversion

%build
cd src
sed -i \
    -e "s,HTTPD_FLAGS=,HTTPD_FLAGS=-I${APACHE24_ROOT}/include -I${OPENSSL_ROOT}/include -I${LIBXML2_ROOT}/include/libxml2/,g" \
    -e "s,apidoc ,,g" \
    Makefile
export PATH=$PATH:$DOXYGEN_ROOT/bin
make %makeprocesses
cd -

%install
export PATH=$PATH:$DOXYGEN_ROOT/bin
DESTDIR=%i make %makeprocesses install

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
