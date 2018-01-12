### RPM cms das v04.01.01
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define pkg DAS
Source0: git://github.com/dmwm/DAS?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
#python2 build
Requires: python cherrypy yui mongo py2-pymongo py2-pystemmer py2-lxml
Requires: py2-pycurl py2-jinja rotatelogs
# keyword search dependencies below
Requires: py2-jsonpath-rw py2-nltk py2-whoosh
Requires: jemalloc

# python3 build
#Requires: python3 py3-cherrypy yui mongo py3-pymongo py3-pystemmer py3-lxml
#Requires: py3-pycurl py3-jinja rotatelogs
## keyword search dependencies below
#Requires: py3-jsonpath-rw py3-nltk py3-whoosh
#Requires: jemalloc

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c

%build
cd DAS
# remove ipython stuff
if [ -f src/python/DAS/tools/ipy_profile_mongo.py ]; then
   rm src/python/DAS/tools/ipy_profile_mongo.py
fi

# setup version
cat src/python/DAS/__init__.py | sed "s,development,%{realversion},g" > init.tmp
mv -f init.tmp src/python/DAS/__init__.py

# do DAS build
python setup.py build
#python3 setup.py build

# set PYTHONPATH since it is used by DAS tools
PYTHONPATH=$PWD/src/python:$PYTHONPATH

# clean-up DAS YML files
rm -rf src/python/DAS/services/{cms_maps,maps}

# build DAS sphinx documentation
export DAS_CONFIG=$PWD/etc/das.cfg
cd doc
mkdir -p sphinx/_static
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build

%install
cd DAS
python setup.py install --prefix=%i
#python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/doc/build/html
mkdir -p doc/build/html
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
