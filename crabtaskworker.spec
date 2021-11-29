### RPM cms crabtaskworker v3.210301

# This specfile accepts both following types of tags:
# - v3.210701 -> builds py2 environment
# - py3.211129 -> build py3 environment

## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define webdoc_files %{installroot}/%{pkgrel}/doc/

%define version_prefix %(echo %{realversion} | cut -d. -f1)
%if "%{version_prefix}" == "py3"
%define python_runtime %(echo python3)
%define wmcrepo mapellidario
%define wmcver 1.5.5
Requires: p5-time-hires
Requires: python3 py3-dbs3-client py3-pycurl py3-httplib2 py3-cherrypy py3-htcondor 
Requires: py3-ldap 
Requires: py3-retry
Requires: py3-rucio-clients py3-future
Requires: jemalloc
%else
%define python_runtime %(echo python)
%define wmcrepo dmwm
%define wmcver 1.4.6.pre2
Requires: p5-time-hires
Requires: python dbs3-client py2-pycurl py2-httplib2 cherrypy condor python-ldap py2-retry
Requires: py2-rucio-clients py2-ipython py2-future
Requires: jemalloc
BuildRequires: py2-sphinx
%endif


Source0: git://github.com/%{wmcrepo}/WMCore.git?obj=master/%{wmcver}&export=WMCore-%{wmcver}&output=/WMCore-%{n}-%{wmcver}.tar.gz
Source1: git://github.com/dmwm/CRABServer.git?obj=master/%{realversion}&export=CRABServer-%{realversion}&output=/CRABServer-%{realversion}.tar.gz
#Patch0: crabtaskworker_cherrypy

#Patch0: crabserver3-setup

%prep
%setup -D -T -b 1 -n CRABServer-%{realversion}
#%patch0 -p0 -d bin
%setup -T -b 0 -n WMCore-%{wmcver}
#%patch0 -p1

%build
touch $PWD/condor_config
export CONDOR_CONFIG=$PWD/condor_config
cd ../WMCore-%{wmcver}
%if "%{version_prefix}" == "py3"
%{python_runtime} setup.py build_system -s crabtaskworker --skip-docs
%else
%{python_runtime} setup.py build_system -s crabtaskworker
%endif
PYTHONPATH=$PWD/build/lib:$PYTHONPATH

cd ../CRABServer-%{realversion}
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/taskworker/conf.py
echo -e "\n__version__ = \"%{realversion}\"#Automatically added during RPM build process" >> src/python/TaskWorker/__init__.py
%if "%{version_prefix}" == "py3"
%{python_runtime} setup.py build_system -s TaskWorker --skip-docs=d
%else
%{python_runtime} setup.py build_system -s TaskWorker
%endif

sed -i 's|CRAB3_VERSION=.*|CRAB3_VERSION=%{realversion}|' bin/htcondor_make_runtime.sh
sed -i 's|CRABSERVERVER=.*|CRABSERVERVER=%{realversion}|' bin/htcondor_make_runtime.sh
sed -i 's|WMCOREVER=.*|WMCOREVER=%{wmcver}|' bin/htcondor_make_runtime.sh

RPM_RELEASE=1 ./bin/htcondor_make_runtime.sh

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
touch $PWD/condor_config
export CONDOR_CONFIG=$PWD/condor_config
cd ../WMCore-%{wmcver}
%{python_runtime} setup.py install_system -s  crabtaskworker --prefix=%i
cd ../CRABServer-%{realversion}
%{python_runtime} setup.py install_system -s TaskWorker  --prefix=%i
cp TaskManagerRun-%{realversion}.tar.gz  %i/data/TaskManagerRun.tar.gz
cp CMSRunAnalysis-%{realversion}.tar.gz  %i/data/CMSRunAnalysis.tar.gz
find %i -name '*.egg-info' -exec rm {} \;

# Generate .pyc files.
%{python_runtime} -m compileall %i/$PYTHON_LIB_SITE_PACKAGES/CRABServer || true

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
