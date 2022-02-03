### RPM cms reqmgr2ms 1.0.0.pre3
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define wmcorever 2.0.0.pre3

Source: git://github.com/dmwm/WMCore?obj=master/%wmcorever&export=%n&output=/%n.tar.gz
Requires: py3-cherrypy py3-pycurl py3-httplib2 py3-rucio-clients py3-retry py3-future
Requires: py3-cmsmonitoring py3-pymongo py3-gfal2-python py3-dbs3-client
Requires: rotatelogs jemalloc mongo
BuildRequires: py3-sphinx

%prep
%setup -b 0 -n %n 

%build
python3 setup.py build_system -s reqmgr2ms --skip-docs

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python3 setup.py install_system -s reqmgr2ms --prefix=%i
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
