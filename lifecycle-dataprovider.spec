### RPM cms lifecycle-dataprovider 1.0.7
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define pkg DataProvider
#%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: https://github.com/dmwm/LifeCycle/archive/%{realversion}.tar.gz
#Source0: git://github.com/dmwm/LifeCycle?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
#Source0: %svnserver/LifeCycle/tags/%{realversion}/DataProvider/?scheme=svn+ssh&strategy=export&module=DataProvider&output=/dataprovider.tar.gz
Requires: python
BuildRequires: py2-sphinx

%prep
%setup -D -T -b 0 -n LifeCycle-%{realversion}

%build
pwd
cd DataProvider

# setup version
cat src/python/DataProvider/__init__.py | sed "s,development,%{realversion},g" > init.tmp
mv -f init.tmp src/python/DataProvider/__init__.py

python setup.py build

# build DataProvider sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html
cd -

%install
pwd
cd DataProvider
python setup.py install --prefix=%i
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
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
## SUBPACKAGE webdoc
