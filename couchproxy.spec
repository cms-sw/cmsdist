### RPM cms couchproxy 0.0.2
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages

Source: https://github.com/stuartw/CouchProxy/tarball/%v

Requires: python py2-httplib2

%prep
%setup -n *-CouchProxy-*

%build

%install

mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
cp -pf %_builddir/*-CouchProxy-*/* %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages/

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh