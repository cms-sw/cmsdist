### RPM cms crab3 3.0.7d
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES

%define webdoc_files %i/doc/
%define wmcver 0.8.25
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_cs3.tar.gz
Source1: %svnserver/CRABServer/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=CRABServer&output=/CRAB3.tar.gz
Requires: python cherrypy py2-cheetah py2-sqlalchemy py2-httplib2 rotatelogs py2-cx-oracle dbs-client py2-sphinx dls-client
Patch0: crab3-setup

%prep
%setup -D -T -b 1 -n CRABServer
%setup -T -b 0 -n WMCore
%patch0 -p0
%build
cd ../WMCore
python setup.py build_system -s crab3 
cd ../CRABServer
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/crabserver/conf.py
python setup.py build_system -s All

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../WMCore
python setup.py install_system -s crab3 --prefix=%i
cd ../CRABServer
python setup.py install_system -s All --prefix=%i
#egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES/CRABServer || true

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%i/
%exclude %i/doc

## SUBPACKAGE webdoc
