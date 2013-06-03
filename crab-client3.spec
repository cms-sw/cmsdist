### RPM cms crab-client3 3.2.0pre5
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES

%define wmcver 0.9.70
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define crabutils 0.0.1pre5

Source0: git://github.com/dmwm/WMCore.git?obj=master/%{wmcver}&export=WMCore-%{wmcver}&output=/WMCore-%{wmcver}.tar.gz
Source1: git://github.com/dmwm/CRABClient.git?obj=master/%{realversion}&export=CRABClient-%{realversion}&output=/CRABClient-%{realversion}.tar.gz

Requires: python py2-httplib2 py2-sphinx py2-pycurl

Patch0: crabserver3-setup

%prep
%setup -D -T -b 1 -n CRABClient-%{realversion}
%setup -T -b 0 -n WMCore-%{wmcver}
%patch0 -p0

%build
##cafutilities
cd ../

#unset SSH_ASKPASS
git clone http://git.cern.ch/pub/CAFUtilities
cd CAFUtilities
git checkout %{crabutils}
cd -
mv CAFUtilities CAFUtilities-%{crabutils}

cd WMCore-%{wmcver}
python setup.py build_system -s crabclient
cd ../CRABClient-%{realversion}
python setup.py build

PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat crabclient/conf.py | sed "s,development,%{realversion},g" > crabclient/conf.py.tmp
mv crabclient/conf.py.tmp crabclient/conf.py
mkdir -p build
make html

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cp -r ../CAFUtilities-%{crabutils}/src/python/PandaServerInterface.py %i/$PYTHON_LIB_SITE_PACKAGES/PandaServerInterface.py
cd ../WMCore-%{wmcver}
python setup.py install_system -s crabclient --prefix=%i
cd ../CRABClient-%{realversion}
python setup.py install --prefix=%i
cp -rp src/python/* %i/$PYTHON_LIB_SITE_PACKAGES/
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES || true
cp -rp bin %i

find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/doc
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

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
