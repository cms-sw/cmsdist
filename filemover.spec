### RPM cms filemover 1.1.11
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define wmcver 0.8.3
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
%define pkg FileMover
Source0: git://github.com/dmwm/FileMover?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Source1: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_fm.tar.gz
Source2: http://github.com/downloads/sstephenson/prototype/prototype_1-6-1.js
Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah yui
Requires: rotatelogs java-jdk srmcp
BuildRequires: py2-sphinx

%prep
%setup -c
%setup -T -D -a 1

%build
cd WMCore
python setup.py build_system -s wmc-web
cd ../FileMover

# setup version
cat src/python/fm/__init__.py | sed "s,development,%{realversion},g" > init.tmp
mv -f init.tmp src/python/fm/__init__.py

rm -f src/js/prototype.js
cp %{_sourcedir}/prototype*.js src/js/prototype.js
python setup.py build

# build FileMover sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

%install
cd WMCore
python setup.py install_system -s wmc-web --prefix=%i
cd ../FileMover
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
