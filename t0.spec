### RPM cms t0 2.1.7
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define webdoc_files %{installroot}/%{pkgrel}/doc/

%define wmcver 1.2.8
%define wmcpkg WMCore
%define pkg T0

Source0: git://github.com/dmwm/T0.git?obj=master/%{realversion}&export=T0-%{realversion}&output=/T0-%{realversion}.tar.gz
Source1: git://github.com/dmwm/WMCore?obj=master/%wmcver&export=%{wmcpkg}_%n&output=/%{wmcpkg}_%n.tar.gz

Requires: python py2-sqlalchemy py2-httplib2 py2-pycurl py2-rucio-clients
Requires: py2-mysqldb py2-cx-oracle py2-cheetah py2-pyOpenSSL
Requires: yui libuuid couchdb15 condor pystack
Requires: dbs3-client py2-pyzmq py2-psutil py2-future py2-retry
Requires: jemalloc cmsmonitoring

BuildRequires: py2-sphinx couchskel 

%prep
%setup -c
%setup -T -D -a 1
#%setup -D -T -b 1 -n T0-%{realversion}
#%setup -T -b 0 -n WMCore-%{wmcver}
#%setup -n T0-%{realversion}

# setup version
#cat src/python/T0/__init__.py | sed "s,development,%{realversion},g" > init.tmp
#mv -f init.tmp src/python/T0/__init__.py

%build
# build T0 system from WMCore
echo "Building t0 system"
cd %{wmcpkg}_%n
python setup.py build_system -s t0
#PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../T0-%{realversion}
pwd

# change version to proper one
sed -i -e "s,development,%{realversion},g" src/python/T0/__init__.py
sed -i -e "s,development,%{realversion},g" doc/sphinx/conf.py
sed -i -e "s,development,%{realversion},g" setup.py

# then build the T0
echo "AMR and now building the T0 itself"
python setup.py build

# build T0 sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
#cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
#mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p sphinx/_static
mkdir -p build
make html

%install
echo "Installing t0 system"
cd %{wmcpkg}_%n
python setup.py install_system -s t0 --prefix=%i
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../T0-%{realversion}

echo "Then installing the T0 itself"
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cp -rpf %_builddir/$RPM_PACKAGE_NAME-$RPM_PACKAGE_VERSION/%{wmcpkg}_%n/bin/* %i/bin/
cp -rpf %_builddir/$RPM_PACKAGE_NAME-$RPM_PACKAGE_VERSION/%{wmcpkg}_%n/etc/* %i/etc/

tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

export PYTHONPATH=$PYTHONPATH:$PWD/src/python:$PWD/../WMCore_t0/src/python

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
