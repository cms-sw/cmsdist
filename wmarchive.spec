### RPM cms wmarchive v00.08.16
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
#%define wmcver 1.1.6
%define wmcver 1.2.8.pre3
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define pkg WMArchive
%define wmcpkg WMCore
Source0: git://github.com/dmwm/WMArchive?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Source1: git://github.com/dmwm/WMCore?obj=master/%wmcver&export=%{wmcpkg}_%n&output=/%{wmcpkg}_%n.tar.gz
#Requires: python py2-pydoop py2-avro py2-pymongo mongo cherrypy py2-py4j py2-stomp java-jdk rotatelogs cmsmonitoring
#BuildRequires: py2-sphinx
Requires: python3 py3-pydoop py3-avro py3-pymongo mongo py3-cherrypy py3-py4j py3-stomp java-jdk rotatelogs cmsmonitoring
BuildRequires: py3-sphinx

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c
%setup -T -D -a 1

%build
cd %{wmcpkg}_%n
python setup.py build_system -s wmc-wmarchive
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
cd %{wmcpkg}_%n
python setup.py install_system -s wmc-wmarchive --prefix=%i
cd ../WMArchive

python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/doc
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

# install static files
mkdir -p %i/data/storage
cp -r src/{js,css,images,templates,maps,sass} %i/data

# generate current schema
mkdir -p %i/data/schemas
export PYTHONPATH=$PYTHONPATH:$PWD/src/python:$PWD/../WMCore_wmarchive/src/python
bin/fwjrschema --fout=%i/data/schemas/fwjr_prod.json
bin/json2avsc --fin=%i/data/schemas/fwjr_prod.json --fout=%i/data/schemas/fwjr_prod.avsc
bin/wmexceptions --fout=%i/data/wmexceptions.json
touch %i/${PYTHON_LIB_SITE_PACKAGES}/WMCore/Services/__init__.py

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
