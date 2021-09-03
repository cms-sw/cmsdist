### RPM cms reqmgr2 1.5.1.cmsweb2
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/dmwm/WMCore?obj=master/%realversion&export=%n&output=/%n.tar.gz

#from private repository
#Source: git://github.com/ticoann/WMCore?obj=reqmgr2_dashboard_dep/%realversion&export=%n&output=/%n.tar.gz

Requires: python3 py3-httplib2 py3-cherrypy py3-cheetah3 py3-pycurl py3-dbs3-client
Requires: py3-future py3-retry py3-psutil py3-cmsmonitoring
Requires: jemalloc rotatelogs couchdb16
BuildRequires: py3-sphinx

%prep
%setup -b 0 -n %n 

%build
python3 setup.py build_system -s reqmgr2 --skip-docs

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python3 setup.py install_system -s reqmgr2 --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pfr %_builddir/%n/bin/[[:lower:]]* %i/bin
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'

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
