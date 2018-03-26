### RPM cms das 05.00.01
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg0 DAS
%define ver0 %realversion
%define pkg1 das2go
%define ver1 03.00.04
Source0: https://github.com/dmwm/%pkg0/archive/%ver0.tar.gz
Source1: https://github.com/dmwm/%pkg1/archive/%ver1.tar.gz

#python2 build
Requires: python cherrypy yui mongo py2-pymongo py2-pystemmer py2-lxml
Requires: py2-pycurl py2-jinja rotatelogs
# keyword search dependencies below
Requires: py2-jsonpath-rw py2-nltk py2-whoosh
Requires: jemalloc

# got das2go we need go language
Requires: go

# python3 build
#Requires: python3 py3-cherrypy yui mongo py3-pymongo py3-pystemmer py3-lxml
#Requires: py3-pycurl py3-jinja rotatelogs
## keyword search dependencies below
#Requires: py3-jsonpath-rw py3-nltk py3-whoosh
#Requires: jemalloc

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 1 -n %pkg1-%ver1
%setup -D -T -b 0 -n %pkg0-%ver0

%build
echo "start das build: $PWD"
cd ../%pkg0-%ver0
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
cd -

# build das2go
cd ..
echo "start das2go build: $PWD"
mkdir -p gopath
export GOPATH=$PWD/gopath
go get github.com/dmwm/cmsauth
go get github.com/dmwm/das2go
go get github.com/vkuznet/x509proxy
go get gopkg.in/mgo.v2
go get github.com/sirupsen/logrus
cd $GOPATH/src/github.com/dmwm/das2go
make
cd -

%install
cd ..
echo "start das install: $PWD"
cd %pkg0-%ver0
python setup.py install --prefix=%i
#python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/doc/build/html
mkdir -p doc/build/html
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

# install das2go
cd ..
echo "start das2go install: $PWD"
export GOPATH=$PWD/gopath
cp $GOPATH/src/github.com/dmwm/das2go/das2go %i/bin
cp $GOPATH/src/github.com/dmwm/das2go/bin/das2go_server %i/bin
mkdir -p %i/das2go/yui
cp -r $GOPATH/src/github.com/dmwm/das2go/{js,css,images,templates} %i/das2go/
export YUI_ROOT
cp -r $YUI_ROOT/build %i/das2go/yui/

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
