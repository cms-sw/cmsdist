### RPM external py2-restkit 2.2.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/r/restkit/restkit-2.2.1.tar.gz#md5=ec79eee99e2128763b9b0493a6aa6d9b 
Requires: python py2-setuptools

%prep
%setup -n restkit-%realversion

%build

%install
# Copy all tar ball files as they may be needed by couchapps while developing
cp -rp %_builddir/restkit-%realversion/* %i/

# Now installs libs as the normal procedure would do. This avoids easy_install
# pkg management. 
python setup.py install_lib --install-dir=%i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

# Cleans unnecessary stuff
rm -rf %i/build %i/debian

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

