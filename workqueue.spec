### RPM cms workqueue 2.1.5rc4
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git+https://github.com/dmwm/WMCore.git?obj=master/%{realversion}&export=%n&output=/%n.tar.gz
Requires: python3 py3-httplib2 py3-dbs3-client py3-cherrypy py3-pycurl
Requires: py3-future py3-retry py3-psutil py3-rucio-clients py3-cmsmonitoring
Requires: jemalloc rotatelogs couchdb yui
BuildRequires: py3-sphinx

%prep
%setup -b 0 -n %n

%build
python3 setup.py build_system -s global-workqueue --skip-docs

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python3 setup.py install_system -s global-workqueue --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pf %_builddir/%n/bin/*workqueue* %i/bin
cp -pf %_builddir/%n/bin/wmagent-couchapp-init %i/bin
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
