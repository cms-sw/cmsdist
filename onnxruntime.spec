### RPM external onnxruntime 1.0.0
%define tag eb635bfb66dae6cf414abfd1eb94c93842f1e66e
%define branch cms/v1.0.0
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja zlib python3
Requires: protobuf


%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build

cmake ../%{n}-%{realversion}/cmake -GNinja \
   -DPYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3 \
   -DCMAKE_BUILD_TYPE=Release \
   -DCMAKE_INSTALL_PREFIX="%{i}" \
   -Donnxruntime_BUILD_SHARED_LIB=ON \
   -Donnxruntime_USE_CUDA=OFF \
   -Donnxruntime_USE_NSYNC=OFF \
   -Donnxruntime_BUILD_CSHARP=OFF \
   -Donnxruntime_USE_AUTOML=OFF \
   -Donnxruntime_USE_EIGEN_FOR_BLAS=ON \
   -Donnxruntime_USE_OPENBLAS=OFF \
   -Donnxruntime_USE_MKLDNN=OFF \
   -Donnxruntime_USE_MKLML=OFF \
   -Donnxruntime_USE_NGRAPH=OFF \
   -Donnxruntime_USE_OPENMP=OFF \
   -Donnxruntime_USE_TVM=OFF \
   -Donnxruntime_USE_LLVM=OFF \
   -Donnxruntime_ENABLE_MICROSOFT_INTERNAL=OFF \
   -Donnxruntime_USE_BRAINSLICE=OFF \
   -Donnxruntime_USE_NUPHAR=OFF \
   -Donnxruntime_USE_EIGEN_THREADPOOL=OFF \
   -Donnxruntime_USE_TENSORRT=OFF \
   -Donnxruntime_CROSS_COMPILING=OFF \
   -Donnxruntime_USE_FULL_PROTOBUF=ON \
   -Donnxruntime_DISABLE_CONTRIB_OPS=OFF \
   -Donnxruntime_BUILD_UNIT_TESTS=OFF \
   -Donnxruntime_USE_PREINSTALLED_PROTOBUF=ON \
   -Dprotobuf_INSTALL_PATH=${PROTOBUF_ROOT}

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
