### RPM cms das 2.2.5
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define wmcver 0.8.3
%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
%define pkg DAS
Source0: git://github.com/dmwm/DAS?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Source1: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_das.tar.gz
Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah yui
Requires: mongo py2-pymongo py2-cjson py2-yaml py2-pystemmer py2-mongoengine py2-lxml py2-ply py2-yajl
Requires: py2-pycurl rotatelogs
# keyword search dependencies below
Requires: py2-jsonpath-rw py2-nltk py2-whoosh
BuildRequires: py2-sphinx

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c
%setup -T -D -a 1

%build
cd WMCore
python setup.py build_system -s wmc-web
cd ../DAS
# remove ipython stuff
if [ -f src/python/DAS/tools/ipy_profile_mongo.py ]; then
   rm src/python/DAS/tools/ipy_profile_mongo.py
fi

# setup version
cat src/python/DAS/__init__.py | sed "s,development,%{realversion},g" > init.tmp
mv -f init.tmp src/python/DAS/__init__.py

# do DAS build
python setup.py build

# build DAS JSON maps out of DAS YML files
cmd="python src/python/DAS/tools/das_drop_maps.py"
dir="src/python/DAS/services/cms_maps/"
map_file="$dir/das_maps.js"
rm -f $map_file
export PYTHONPATH=$PYTHONPATH:$PWD/src/python
for amap in `ls $dir/*.yml`
do
    $cmd --uri-map=$amap >> $map_file
    $cmd --notation-map=$amap >> $map_file
    $cmd --presentation-map=$amap >> $map_file
done
cat $map_file | grep -v "###" > $map_file.tmp
rm -f $map_file
mv $map_file.tmp $map_file
rm -f $dir/*.yml
rm -rf src/python/DAS/services/maps

# build DAS sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

%install
cd WMCore
python setup.py install_system -s wmc-web --prefix=%i
cd ../DAS
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
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
## SUBPACKAGE webdoc
