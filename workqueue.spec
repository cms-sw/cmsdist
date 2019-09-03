### RPM cms workqueue 1.2.6.pre4
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/dmwm/WMCore.git?obj=master/%{realversion}&export=%n&output=/%n.tar.gz
Requires: python py2-httplib2 pystack rotatelogs couchdb15 yui py2-sphinx dbs3-client py2-cherrypy py2-pycurl
Requires: py2-future py2-retry py2-psutil py2-rucio-clients
Requires: jemalloc cmsmonitoring

%prep
%setup -b 0 -n %n

%build
python setup.py build_system -s workqueue

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s workqueue --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pf %_builddir/%n/bin/*workqueue* %i/bin
cp -pf %_builddir/%n/bin/wmagent-couchapp-init %i/bin

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
