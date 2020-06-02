############## IMPORTANT #################
#For new crabserver tag in github, set the version_suffix to 00
#For any other change, increment version_suffix
##########################################
%define version_suffix 00
%define crabserver_tag 3.200531
### RPM cms crabcache %{crabserver_tag}.%{version_suffix}
# note, the above line will define %{crabserver_tag}=%{crabserver_tag}.%{version_suffix}

## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 1.3.3

Source0: git://github.com/dmwm/WMCore.git?obj=master/%{wmcver}&export=WMCore-%{wmcver}&output=/WMCore-%{n}-%{wmcver}.tar.gz
Source1: git://github.com/dmwm/CRABServer.git?obj=master/%{crabserver_tag}&export=CRABServer-%{crabserver_tag}&output=/CRABServer-%{crabserver_tag}.tar.gz

Requires: python cherrypy py2-cjson rotatelogs py2-pycurl py2-httplib2 py2-sqlalchemy py2-cx-oracle
BuildRequires: py2-sphinx
#Patch0: crabserver3-setup

%prep

if [ "%{v}" != "%{realversion}" ] ; then
  echo "ERROR: %{v} not same as %{realversion}. Please increment version suffix in %{n}.spec file."
  exit 1
fi

%setup -D -T -b 1 -n CRABServer-%{crabserver_tag}
%setup -T -b 0 -n WMCore-%{wmcver}
#%patch0 -p1

%build
cd ../WMCore-%{wmcver}
python setup.py build_system -s crabcache

cd ../CRABServer-%{crabserver_tag}
perl -p -i -e "s{<VERSION>}{%{crabserver_tag}}g" doc/crabserver/conf.py
echo "__version__ = \"%{crabserver_tag}\"#Automatically added during RPM build process" >> src/python/UserFileCache/__init__.py
python setup.py build_system -s UserFileCache

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../WMCore-%{wmcver}
python setup.py install_system -s crabcache --prefix=%i
cd ../CRABServer-%{crabserver_tag}
python setup.py install_system -s UserFileCache --prefix=%i
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
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
