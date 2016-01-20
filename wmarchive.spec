### RPM cms wmarchive v00.00.03
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define wmcver 1.0.13.pre6
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define pkg WMArchive
%define wmcpkg WMCore
Source0: git://github.com/dmwm/WMArchive?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Source1: git://github.com/dmwm/WMCore?obj=master/%wmcver&export=%wmcpkg&output=/%wmcpkg.tar.gz
Requires: python py2-pydoop py2-avro py2-pymongo mongo py2-httplib2 cherrypy rotatelogs
BuildRequires: py2-sphinx

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c
%setup -T -D -a 1

%build
cd WMCore
python setup.py build_system -s wmc-rest
cd ../WMArchive

# change version to proper one
sed -i -e "s,development,%{realversion},g" src/python/WMArchive/__init__.py
sed -i -e "s,development,%{realversion},g" doc/sphinx/conf.py
sed -i -e "s,development,%{realversion},g" setup.py

# do WMArchive build
python setup.py build

# build WMArchive sphinx documentation
cd doc
mkdir -p sphinx/_static
mkdir -p build
make html

%install
cd WMCore
python setup.py install_system -s wmc-rest --prefix=%i
cd ../WMArchive

python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/doc
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

# install static files
mkdir -p %i/data/storage
cp -r src/{js,css,images,templates} %i/data

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
