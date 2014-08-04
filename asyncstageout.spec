### RPM cms asyncstageout 1.0.3pre1
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PERL5LIB %i/Monitor/perl_lib

%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 0.9.95e

Source0: git://github.com/dmwm/WMCore.git?obj=master/%{wmcver}&export=WMCore-%{wmcver}&output=/WMCore-%{wmcver}.tar.gz
Source1: git://github.com/dmwm/AsyncStageout.git?obj=master/%{realversion}&export=AsyncStageout-%{realversion}&output=/AsyncStageout-%{realversion}.tar.gz
Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 rotatelogs pystack py2-sphinx dbs-client couchdb py2-pycurl couchskel py2-stomp dbs3-client
Requires: PHEDEX-micro PHEDEX-lifecycle

%prep
%setup -D -T -b 1 -n AsyncStageout-%{realversion}
%setup -T -b 0 -n WMCore-%{wmcver}

%build
cd ../WMCore-%{wmcver}
python setup.py build_system -s asyncstageout
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../AsyncStageout-%{realversion}
python setup.py build

PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat asyncstageout/conf.py | sed "s,development,%{realversion},g" > asyncstageout/conf.py.tmp
mv asyncstageout/conf.py.tmp asyncstageout/conf.py
mkdir -p build
make html

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../WMCore-%{wmcver}
python setup.py install_system -s asyncstageout --prefix=%i
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../AsyncStageout-%{realversion}
python setup.py install --prefix=%i
cp -pr ../AsyncStageout-%{realversion}/src/python/AsyncStageOut %i/$PYTHON_LIB_SITE_PACKAGES/
cp -pr ../AsyncStageout-%{realversion}/src/couchapp %i/
cp -pr ../AsyncStageout-%{realversion}/bin %i/
cp -pr ../AsyncStageout-%{realversion}/configuration %i/
cp -pr ../AsyncStageout-%{realversion}/src/Monitor %i/
find %i -name '*.egg-info' -exec rm {} \;

# Pick external dependencies from couchskel
mkdir %i/couchapp/UserMonitoring/vendor/
cp -rp $COUCHSKEL_ROOT/data/couchapps/couchskel/vendor/{couchapp,jquery,datatables} \
  %i/couchapp/UserMonitoring/vendor/

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES/AsyncStageOut || true

#mkdir -p %i/bin
cp -pf %_builddir/WMCore-%{wmcver}/bin/{wmcoreD,wmcore-new-config,wmagent-mod-config,wmagent-couchapp-init} %i/bin/

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
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
