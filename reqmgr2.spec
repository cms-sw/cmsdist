### RPM cms reqmgr2 1.2.6.pre2
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/dmwm/WMCore?obj=master/%realversion&export=%n&output=/%n.tar.gz

#from private repository
#Source: git://github.com/ticoann/WMCore?obj=reqmgr2_dashboard_dep/%realversion&export=%n&output=/%n.tar.gz

Requires: py2-httplib2 py2-cherrypy py2-cheetah rotatelogs couchdb15 py2-sphinx py2-pycurl dbs3-client
Requires: py2-future py2-retry py2-psutil
Requires: jemalloc cmsmonitoring

%prep
%setup -b 0 -n %n 

%build
python setup.py build_system -s reqmgr2

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s reqmgr2 --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pfr %_builddir/%n/bin/[[:lower:]]* %i/bin

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
