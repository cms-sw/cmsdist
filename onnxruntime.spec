### RPM external onnxruntime 0.4.0
%define tag %{realversion}
%define branch master
%define github_user microsoft
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/v%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja zlib python3

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build

cmake ../%{n}-%{realversion}/cmake -GNinja \
   -DCMAKE_BUILD_TYPE=Release \
   -DCMAKE_INSTALL_PREFIX="%{i}" \
   -Donnxruntime_BUILD_SHARED_LIB=ON \
   -Donnxruntime_USE_CUDA=OFF \
   -Donnxruntime_USE_NSYNC=OFF \
   -Donnxruntime_BUILD_CSHARP=OFF \
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
   -Donnxruntime_USE_FULL_PROTOBUF=OFF \
   -Donnxruntime_DISABLE_CONTRIB_OPS=OFF \
   -Donnxruntime_BUILD_UNIT_TESTS=OFF

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install

