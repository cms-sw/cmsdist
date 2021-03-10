### RPM cms wmagentpy3 1.4.7.pre2
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/dmwm/WMCore.git?obj=master/%{realversion}&export=WMCore-%{realversion}&output=/WMCore-%{realversion}.tar.gz

Requires: yui libuuid couchdb15 condor jemalloc dbs3-client
Requires: python3 py3-sqlalchemy py3-httplib2 py3-pycurl py3-rucio-clients
Requires: py3-cx-oracle py3-jinja2 py3-pyOpenSSL
Requires: py3-pyzmq py3-psutil py3-future py3-retry
Requires: py3-cmsmonitoring
# Alan Malta dropped on 2/Feb/2021: Requires: py3-cheetah py3-mysqldb
BuildRequires: py3-sphinx couchskel

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
