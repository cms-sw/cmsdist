### RPM external mxnet-predict 1.5.0
## INITENV +PATH PYTHON27PATH %{i}/lib64/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
## INITENV +PATH PYTHON3PATH %{i}/lib64/python`echo $PYTHON3_VERSION | cut -d. -f 1,2`/site-packages
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64

%define tag 337cf1b54cc02bde94f459c89863a18187b0aada
%define branch 1.5.0-cms-mod
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
rm %{i}/lib64/*.a %{i}/*.so
mv %{i}/python* %{i}/lib64
