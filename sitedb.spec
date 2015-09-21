### RPM cms sitedb 2.6.3
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 1.0.10.pre2

Source0: git://github.com/dmwm/WMCore?obj=master/%wmcver&export=wmcore_%n&output=/wmcore_%n.tar.gz
Source1: git://github.com/dmwm/sitedb?obj=master/%realversion&export=%n&output=/%n.tar.gz
#Source1: git://github.com/juztas/sitedb?obj=master/%realversion&export=%n&output=/%n.tar.gz
#Source1: https://cern.ch/lat/temp/sitedb5.tar.gz

Requires: cherrypy yui3 d3 xregexp py2-cx-oracle py2-cjson py2-pycurl python-ldap rotatelogs
BuildRequires: wmcore-devtools

%prep
%setup -T -b 0 -n wmcore_%n
%setup -D -T -b 1 -n %n
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/conf.py

%build
cd ../wmcore_%n
python setup.py build_system -s wmc-rest
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../%n
export SITEDB_VERSION=%realversion
python setup.py build_system --compress

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}${PYTHON_LIB_SITE_PACKAGES}
cd ../wmcore_%n
python setup.py install_system -s wmc-rest --prefix=%i
cd ../%n
python setup.py install_system --compress --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate an env.sh which sets a few things more than init.sh.
(echo ". %i/etc/profile.d/init.sh;"
 echo "export YUI3_ROOT D3_ROOT XREGEXP_ROOT SITEDB_ROOT SITEDB_VERSION;") > %i/etc/profile.d/env.sh

%post
%{relocateConfig}etc/profile.d/{env,dep*}.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
