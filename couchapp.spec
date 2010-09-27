### RPM external couchapp 0.7.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://github.com/couchapp/couchapp/tarball/%realversion?output=/%n-%realversion.tgz
Requires: python py2-setuptools py2-restkit

%prep
%setup -n couchapp-couchapp-202bba1

%build

%install
# Copy all files as requested by Simon
cp -rp %_builddir/couchapp-couchapp-202bba1/* %i/

# Now build/install as normal procedure would do. But
# does each part separately because the general 'install' procedure downloads
# things from elsewhere and uses easy_install pkg management
python setup.py install_lib --install-dir=%i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py install_data --install-dir=%i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
#python setup.py install_scripts --install-dir=%i/bin

# Setups properly the couchapp script because the default one is
# easy_install dependent
(echo '#!/usr/bin/env python'; cat %i/bin/couchapp.py) > %i/bin/couchapp
chmod +x %i/bin/couchapp 

# Cleans unnecessary stuff
rm -rf %i/build %i/debian %i/contrib %i/bin/couchapp.py

# Generates dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
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

