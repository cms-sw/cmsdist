### RPM cms wmagentpy3 1.4.9.pre2
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/dmwm/WMCore.git?obj=master/%{realversion}&export=WMCore-%{realversion}&output=/WMCore-%{realversion}.tar.gz

# Alan on 19/05/2021: commenting out condor for now, otherwise it will bring in some python2 dependencies
# Requires: condor
Requires: yui libuuid couchdb16 jemalloc py3-dbs3-client
Requires: python3 py3-sqlalchemy py3-httplib2 py3-pycurl py3-rucio-clients
Requires: py3-cx-oracle py3-jinja2 py3-pyOpenSSL
Requires: py3-pyzmq py3-psutil py3-future py3-retry
Requires: py3-cmsmonitoring py3-cmscouchapp
Requires: py3-cheetah3
Requires: py3-mysqlclient
Requires: mariadb

# Alan Malta dropped on 2/Feb/2021: Requires: py3-mysqldb
BuildRequires: py3-sphinx couchskel

%prep
%setup -b 0 -n WMCore-%{realversion}

%build
python3 setup.py build

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python3 setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'
find %i -name '*.egg-info' -exec rm {} \;

# Pick external dependencies from couchskel
mkdir %i/data/couchapps/WMStats/vendor/
cp -rp $COUCHSKEL_ROOT/data/couchapps/couchskel/vendor/{couchapp,jquery,datatables} \
  %i/data/couchapps/WMStats/vendor/
