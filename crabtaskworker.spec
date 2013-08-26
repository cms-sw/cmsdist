### RPM cms crabtaskworker 0.0.1pre16
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES


%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 0.9.78
%define crabutils 0.0.1pre16

Source0: git://github.com/dmwm/WMCore.git?obj=master/%{wmcver}&export=WMCore-%{wmcver}&output=/WMCore-%{n}-%{wmcver}.tar.gz
Source1: git+http://git.cern.ch/pub/CAFTaskWorker.git?obj=master/%{realversion}&export=CAFTaskWorker-%{realversion}&output=/CAFTaskWorker-%{realversion}.tar.gz
Source2: git+http://git.cern.ch/pub/CAFUtilities.git?obj=master/%{crabutils}&export=CAFUtilities-%{crabutils}&output=/CAFUtilities-%{crabutils}.tar.gz

Requires: python  dbs-client dls-client dbs3-client py2-pycurl py2-httplib2 py2-sqlalchemy py2-cx-oracle
BuildRequires: py2-sphinx
Patch0: crabtaskworker-setup

%prep
%setup -D -T -b 1 -n CAFTaskWorker-%{realversion}
%setup -T -b 2 -n CAFUtilities-%{crabutils}
%setup -T -b 0 -n WMCore-%{wmcver}
%patch0 -p0

%build
pwd
cd ../WMCore-%{wmcver}
python setup.py build_system -s crabtaskworker 
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../CAFUtilities-%{crabutils}
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/crabutilities/conf.py
python setup.py build_system -s CAFTaskWorker

cd ../CAFTaskWorker-%{realversion}
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/taskworker/conf.py
python setup.py build_system -s CAFTaskWorker

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../WMCore-%{wmcver}
python setup.py install_system -s  crabtaskworker --prefix=%i
cd ../CAFUtilities-%{crabutils}
python setup.py install_system -s CAFTaskWorker  --prefix=%i
cd ../CAFTaskWorker-%{realversion}
python setup.py install_system -s CAFTaskWorker  --prefix=%i

find %i -name '*.egg-info' -exec rm {} \;

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES/CAFTaskWorker || true

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
