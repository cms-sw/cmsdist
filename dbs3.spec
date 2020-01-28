### RPM cms dbs3 3.10.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV SET DBS3_SERVER_ROOT %i/
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 1.2.3.dbs2

Source0: git://github.com/dmwm/WMCore.git?obj=1.2.3_dbs/%{wmcver}&export=WMCore&output=/WMCore4%{n}.tar.gz
Source1: git://github.com/dmwm/DBS.git?obj=master/%{realversion}&export=DBS&output=/%{n}.tar.gz

Requires: python py2-simplejson py2-sqlalchemy096 py2-httplib2 cherrypy py2-cheetah yui
Requires: py2-cjson py2-cx-oracle py2-docutils dbs3-pycurl-client rotatelogs pystack cmsmonitoring
Requires: jemalloc
BuildRequires: py2-sphinx

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n DBS

%build
cd ../WMCore
python setup.py build_system -s wmc-web
cd ../DBS
python setup.py build_system -s dbs-web
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../WMCore
python setup.py install_system -s wmc-web --prefix=%i
cd ../DBS
python setup.py install_system -s dbs-web --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

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

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
## SUBPACKAGE webdoc
