### RPM cms t0 3.0.8
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define webdoc_files %{installroot}/%{pkgrel}/doc/

%define wmcver 2.1.6.3
%define wmcpkg WMCore
%define pkg T0

Source0: git+https://github.com/dmwm/T0.git?obj=master/%{realversion}&export=T0-%{realversion}&output=/T0-%{realversion}.tar.gz
Source1: git+https://github.com/dmwm/WMCore.git?obj=master/%wmcver&export=%{wmcpkg}_%n&output=/%{wmcpkg}_%n.tar.gz

Requires: python3 py3-sqlalchemy py3-httplib2 py3-pycurl py3-rucio-clients
Requires: py3-mysqlclient py3-cx-oracle py3-cheetah3 py3-pyOpenSSL py3-retry
Requires: py3-dbs3-client py3-pyzmq py3-psutil py3-future py3-cmsmonitoring py3-pyjwt
Requires: yui libuuid couchdb condorpy3 jemalloc

BuildRequires: py3-sphinx py3-sphinxcontrib-websupport couchskel

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
echo "Building T0 system"
cd %{wmcpkg}_%n
python3 setup.py build_system -s t0-agent --skip-docs
#PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../T0-%{realversion}
pwd

# change version to proper one
sed -i -e "s,development,%{realversion},g" src/python/T0/__init__.py
sed -i -e "s,development,%{realversion},g" doc/sphinx/conf.py
sed -i -e "s,development,%{realversion},g" setup.py

# then build the T0
echo "Building T0"
python3 setup.py build

# build T0 sphinx documentation
echo "Building documentation"
#PYTHONPATH=$PWD/src/python:$PYTHONPATH
#cd doc
##cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
##mv sphinx/conf.py.tmp sphinx/conf.py
#mkdir -p sphinx/_static
#mkdir -p build
#make html

%install
echo "Installing T0 system"
cd %{wmcpkg}_%n
python3 setup.py install_system -s t0-agent --prefix=%i
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../T0-%{realversion}

echo "Installing T0"
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
#egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'

mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cp -rpf %_builddir/$RPM_PACKAGE_NAME-$RPM_PACKAGE_VERSION/%{wmcpkg}_%n/bin/* %i/bin/
cp -rpf %_builddir/$RPM_PACKAGE_NAME-$RPM_PACKAGE_VERSION/%{wmcpkg}_%n/etc/* %i/etc/
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'

# Commenting this out, otherwise: tar: doc/build/html: Cannot open: No such file or directory
#tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

export PYTHONPATH=$PYTHONPATH:$PWD/src/python:$PWD/../WMCore_t0/src/python

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
# ## SUBPACKAGE webdoc
