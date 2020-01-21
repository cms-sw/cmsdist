### RPM cms das 04.06.01
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg0 das2go
%define ver0 %realversion
%define pkg1 DASTools
%define ver1 00.01.01
Source0: https://github.com/dmwm/%pkg0/archive/%ver0.tar.gz
Source1: https://github.com/dmwm/%pkg1/archive/%ver1.tar.gz

Requires: go jemalloc yui mongo rotatelogs

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 1 -n %pkg1-%ver1
%setup -D -T -b 0 -n %pkg0-%ver0

%build
cd ..
mkdir -p gopath
export GOPATH=$PWD/gopath
cdir=$PWD

# build das tools
echo "start DASTools build: $PWD"
git clone https://github.com/dmwm/DASTools.git
cd DASTools
git checkout tags/%ver1 -b %ver1
go mod download
make
cd -

# build das2go
echo "start das2go build: $PWD"
git clone https://github.com/dmwm/das2go.git
cd das2go
git checkout tags/%ver0 -b %ver0
make
go build monitor/das2go_monitor.go
cd -

# get FlameGraph
cd $cdir
#cd $GOPATH
git clone https://github.com/brendangregg/FlameGraph.git

# get go-torch
go get github.com/uber/go-torch
go get github.com/shirou/gopsutil
go get github.com/divan/expvarmon

%install
# install das2go
cd ..
cdir=$PWD
echo "start das2go install: $PWD"
ls
export GOPATH=$PWD/gopath
mkdir -p %i/bin
cp das2go/das2go %i/bin
cp das2go/das2go_monitor %i/bin
cp $GOPATH/bin/go-torch %i/bin
cp FlameGraph/*.pl %i/bin
mkdir -p %i/das2go/yui
cp -r das2go/{js,css,images,templates} %i/das2go/
export YUI_ROOT
cp -r $YUI_ROOT/build %i/das2go/yui/

# external tools
cp $GOPATH/bin/expvarmon %i/bin

# install das tools
echo "start DASTools install: $PWD"
cp $cdir/DASTools/bin/* %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
