### RPM external mxnet-predict 1.6.0
## INITENV +PATH PYTHON27PATH %{i}/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHON3PATH %{i}/$PYTHON3_LIB_SITE_PACKAGES
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib

%define tag b4aada51b4af56a05adc4ed17f77001bfd6943d8
%define branch 1.6.0
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/incubator-mxnet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: cmake ninja

Requires: OpenBLAS python python3 py2-numpy py3-numpy

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build

# use LAPACK functions in OpenBLAS:
# manually set MXNET_USE_LAPACK=1 and turn off USE_LAPACK in cmake
export CFLAGS="-DMXNET_USE_LAPACK=1 -DMXNET_THREAD_LOCAL_ENGINE=1"
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
export PYTHON3V=$(echo $PYTHON3_VERSION | cut -f1,2 -d.)

cmake ../%{n}-%{realversion} -GNinja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR="%{i}/lib" \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_CUDA=OFF \
    -DUSE_OPENCV=OFF \
    -DUSE_OPENMP=OFF \
    -DUSE_BLAS=open \
    -DUSE_LAPACK=OFF \
    -DUSE_MKL_IF_AVAILABLE=OFF \
    -USE_MKLDNN=OFF \
    -DUSE_F16C=OFF \
    -DUSE_CPP_PACKAGE=ON \
    -DBUILD_CPP_EXAMPLES=OFF \
    -DCMAKE_LIBRARY_OUTPUT_DIRECTORY="%{i}" \
    -DINSTALL_PYTHON_VERSIONS="${PYTHONV};${PYTHON3V}" \
    -DCMAKE_PREFIX_PATH="${OPENBLAS_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
rm %{i}/*.so
mv %{i}/python* %{i}/lib
