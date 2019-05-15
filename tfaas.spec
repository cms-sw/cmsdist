### RPM cms tfaas 01.00.05
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg0 TFaaS
%define ver0 v%realversion
Source: https://github.com/vkuznet/%pkg0/archive/%ver0.tar.gz
Requires: autotools go rotatelogs

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
#%setup -b 0 -n %n 
%setup -D -T -b 0 -n %pkg0-%realversion

%build
BUILD_DIR=$PWD
echo "start tfaas build: $PWD"
mkdir -p gopath
export GOPATH=$PWD/gopath
go get github.com/dmwm/cmsauth
go get github.com/vkuznet/x509proxy
go get github.com/sirupsen/logrus
go get github.com/shirou/gopsutil

# download and insta TensorFlow libraries
# https://www.tensorflow.org/versions/master/install/install_go
WDIR=$PWD
TF_LIB="libtensorflow-cpu-linux-x86_64-1.13.1.tar.gz"
curl -k -L -O "https://storage.googleapis.com/tensorflow/libtensorflow/${TF_LIB}"
tar xfz $TF_LIB
export LIBRARY_PATH="${WDIR}/lib:${LIBRARY_PATH}"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${WDIR}/lib"
go get github.com/tensorflow/tensorflow/tensorflow/go
go get github.com/tensorflow/tensorflow/tensorflow/go/op

# install protobuf
rm -rf protobuf
git clone https://github.com/google/protobuf.git
cd ${WDIR}/protobuf
./autogen.sh
./configure --prefix=${WDIR}
make
make install
go get -u github.com/golang/protobuf/protoc-gen-go

# build tfaas
cd $WDIR/src/Go
sed -i -e "s,TAG := \$(shell git tag | sort -r | head -n 1),TAG := {TAG},g" Makefile
export TAG=%realversion
sed -i -e "s,{TAG},$TAG,g" Makefile
make

%install
echo "start tfaas install: $PWD"
echo "build dir $BUILD_DIR"
mkdir -p %i/bin
mkdir -p %i/lib
mkdir -p %i/include
mkdir -p %i/static
mkdir -p %i/models
cp src/Go/tfaas %i/bin
cp -r lib/* %i/lib/
cp -r include/* %i/include/
cp -r src/Go/static %i

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
