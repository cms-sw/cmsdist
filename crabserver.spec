### RPM cms crabserver 3.1.1
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES
#

#REMOVE
#%define gitversion github.0.0.1pre28

%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 0.9.0
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_ci.tar.gz
#REMOVE
#Source0: https://github.com/ticoann/WMCore/tarball/v0.0.1pre28?output=/%n-%gitversion.tgz
Source1: https://github.com/lat/WMCore/zipball/f2fccdc7727e1a4acfdaf4df648e67ee184e0911#/wmcore_sitedb.zip
Source2: %svnserver/CRABServer/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=CRABServer&output=/CRABInterface.tar.gz
Requires: python cherrypy py2-cjson rotatelogs py2-pycurl py2-httplib2 py2-sqlalchemy py2-cx-oracle
BuildRequires: py2-sphinx
Patch0: crabserver3-setup

%prep
%setup -D -T -b 2 -n CRABServer
#%setup -D -T -b 1 -n WMCore
%setup -T -b 1 -n lat-WMCore-f2fccdc
%setup -T -b 0 -n WMCore
%patch0 -p0

%build
cd ../WMCore
cp -r ../lat-WMCore-f2fccdc/src/python/WMCore/REST src/python/WMCore/
cp -r ../lat-WMCore-f2fccdc/bin/wmc-httpd bin/wmc-httpd
python setup.py build_system -s crabserver
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../CRABServer
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/crabserver/conf.py
python setup.py build_system -s CRABInterface

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../WMCore
python setup.py install_system -s crabserver --prefix=%i
cp -pr src/couchapps %i/
cd ../CRABServer
python setup.py install_system -s CRABInterface --prefix=%i

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
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
