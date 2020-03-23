### RPM external onnxruntime 1.0.0
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define tag 0f048da7774428d5fb2c4c808fc5820809ab24b8
%define branch cms/v1.0.0_pb380
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja
Requires: protobuf py3-numpy py2-onnx zlib libpng

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build

cmake ../%{n}-%{realversion}/cmake -GNinja \
   -DPYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3 \
   -DCMAKE_BUILD_TYPE=Release \
   -DCMAKE_INSTALL_PREFIX="%{i}" \
   -DCMAKE_INSTALL_LIBDIR=lib \
   -Donnxruntime_BUILD_UNIT_TESTS=ON \
   -Donnxruntime_ENABLE_PYTHON=ON \
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
   -Donnxruntime_USE_PREINSTALLED_PROTOBUF=ON \
   -Dprotobuf_INSTALL_PATH=${PROTOBUF_ROOT} \
   -DCMAKE_PREFIX_PATH="${ZLIB_ROOT};${LIBPNG_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)
python3 ../%{n}-%{realversion}/setup.py build

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
mkdir -p %{i}/${PYTHON3_LIB_SITE_PACKAGES}
mv build/lib/onnxruntime %{i}/${PYTHON3_LIB_SITE_PACKAGES}/
