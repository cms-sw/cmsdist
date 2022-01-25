### RPM cms crabserver py3.220124

# This specfile accepts both following types of tags:
# - v3.210701 -> builds py2 environment
# - py3.211104patch1 -> build py3 environment

## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define webdoc_files %{installroot}/%{pkgrel}/doc/

%define version_prefix %(echo %{realversion} | cut -d. -f1)
%if "%{version_prefix}" == "py3"
%define python_runtime %(echo python3)
%define wmcrepo dmwm
%define wmcver 1.5.7
%define crabrepo dmwm
Requires: python3 py3-cherrypy py3-pycurl py3-cx-oracle
Requires: py3-retry py3-boto3 py3-future py3-pyOpenSSL py3-htcondor rotatelogs jemalloc
BuildRequires: py3-sphinx
%else
%define python_runtime %(echo python)
%define wmcrepo dmwm
%define wmcver 1.4.6.crab1
%define crabrepo dmwm
Requires: python py2-ipython py2-cherrypy py2-cjson rotatelogs py2-pycurl py2-cx-oracle
Requires: py2-pyOpenSSL condor dbs3-pycurl-client dbs3-client py2-retry py2-future
Requires: py2-boto3
Requires: jemalloc
BuildRequires: py2-sphinx
%endif
#Patch1: crabserver3-setup

Source0: git://github.com/%{wmcrepo}/WMCore.git?obj=master/%{wmcver}&export=WMCore-%{wmcver}&output=/WMCore-%{n}-%{wmcver}.tar.gz
Source1: git://github.com/%{crabrepo}/CRABServer.git?obj=master/%{realversion}&export=CRABServer-%{realversion}&output=/CRABServer-%{realversion}.tar.gz

%prep
%setup -D -T -b 1 -n CRABServer-%{realversion}
%setup -T -b 0 -n WMCore-%{wmcver}
#%patch1 -p1

%build
touch $PWD/condor_config
export CONDOR_CONFIG=$PWD/condor_config
cd ../WMCore-%{wmcver}
%if "%{version_prefix}" == "py3"
%{python_runtime} setup.py build_system -s crabserver --skip-docs
%else
%{python_runtime} setup.py build_system -s crabserver
%endif
PYTHONPATH=$PWD/build/lib:$PYTHONPATH

cd ../CRABServer-%{realversion}
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/crabserver/conf.py
echo -e "\n__version__ = \"%{realversion}\"#Automatically added during RPM build process" >> src/python/CRABInterface/__init__.py
%if "%{version_prefix}" == "py3"
%{python_runtime} setup.py build_system -s CRABInterface --skip-docs=d
%else
%{python_runtime} setup.py build_system -s CRABInterface
%endif

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
touch $PWD/condor_config
export CONDOR_CONFIG=$PWD/condor_config
cd ../WMCore-%{wmcver}
%{python_runtime} setup.py install_system -s crabserver --prefix=%i
cd ../CRABServer-%{realversion}
%{python_runtime} setup.py install_system -s CRABInterface --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

%if "%{version_prefix}" == "py3"
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'
%endif

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
