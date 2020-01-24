### RPM cms wmagent 1.3.0.pre4
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/dmwm/WMCore.git?obj=master/%{realversion}&export=WMCore-%{realversion}&output=/WMCore-%{realversion}.tar.gz

Requires: python py2-sqlalchemy py2-httplib2 py2-pycurl py2-rucio-clients
Requires: py2-mysqldb py2-cx-oracle py2-cheetah py2-pyOpenSSL
Requires: yui libuuid couchdb15 condor pystack
Requires: dbs3-client py2-pyzmq py2-psutil py2-future py2-retry
Requires: jemalloc cmsmonitoring

BuildRequires: py2-sphinx couchskel

%prep
%setup -b 0 -n WMCore-%{realversion}

%build
python setup.py build

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

# Pick external dependencies from couchskel
mkdir %i/data/couchapps/WMStats/vendor/
cp -rp $COUCHSKEL_ROOT/data/couchapps/couchskel/vendor/{couchapp,jquery,datatables} \
  %i/data/couchapps/WMStats/vendor/

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
