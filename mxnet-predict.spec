### RPM external mxnet-predict 1.5.0
%define tag 337cf1b54cc02bde94f459c89863a18187b0aada
%define branch 1.5.0-cms-mod
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/incubator-mxnet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: cmake ninja ccache

Requires: OpenBLAS lapack

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build

export CFLAGS="-I$OPENBLAS_ROOT/include -I$LAPACK_ROOT/include -DMXNET_THREAD_LOCAL_ENGINE=1"
export LDFLAGS="-L$OPENBLAS_ROOT/lib -L$LAPACK_ROOT/lib64"

cmake ../%{n}-%{realversion} -GNinja \
    -DCMAKE_CUDA_COMPILER_LAUNCHER=ccache \
    -DCMAKE_C_COMPILER_LAUNCHER=ccache \
    -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_CUDA=OFF \
    -DUSE_OPENCV=OFF \
    -DUSE_OPENMP=OFF \
    -DUSE_BLAS=open \
    -DUSE_MKL_IF_AVAILABLE=OFF \
    -USE_MKLDNN=OFF \
    -DUSE_F16C=OFF \
    -DUSE_CPP_PACKAGE=ON \
    -DBUILD_CPP_EXAMPLES=OFF \
    -DCMAKE_PREFIX_PATH="${OPENBLAS_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
rm %{i}/lib64/*.a

