### RPM external jemalloc 5.2.0
Source: https://github.com/jemalloc/jemalloc/archive/%realversion.zip
Requires: gcc autotools

%prep
%setup -n %n-%{realversion}

%build
./autogen.sh \
  --enable-autogen \
  --enable-stats \
  --enable-prof \
  --prefix %i

%install
make
# we explicitly avoid building docs which requires xslt suite to be presented on a system
make install_bin install_include install_lib

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
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
