### RPM cms dbs3 3.0.19
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES
## INITENV SET DBS3_SERVER_ROOT %i/
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 0.9.13
%define cvstag %(echo %{realversion} | sed 's/[.]/_/g; s/^/DBS_/')
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
%define gitserver https://nodeload.github.com
Source0: %gitserver/dmwm/WMCore/tarball/%{wmcver}
Source1: %svnserver/DBS/tags/%cvstag?scheme=svn+ssh&strategy=export&module=DBS3&output=/%{n}.tar.gz

Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah yui
Requires: py2-cjson py2-mysqldb py2-cx-oracle rotatelogs
BuildRequires: py2-sphinx

%prep
%setup -c
%setup -D -T -a 0
%setup -D -T -a 1
# move github directory
mv dmwm-WMCore* WMCore

%build
cd WMCore
python setup.py build_system -s wmc-web
cd ../DBS3
python setup.py build_system -s Server

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd WMCore
python setup.py install_system -s wmc-web --prefix=%i
cd ../DBS3
python setup.py install_system -s Server --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

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

# Exclude Migration server from official rpms 
%exclude %{installroot}/%{pkgrel}/lib/python2.6/site-packages/dbs/web/DBSMigrateModel.py
## SUBPACKAGE webdoc
