### RPM external onnxruntime 1.3.0
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define tag 9294d790219aa0d1007d918d7d736d7f5d3e82d8
%define branch cms/v1.3.0
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja
Requires: protobuf py3-numpy py2-wheel py2-onnx zlib libpng py2-pybind11

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build

cmake ../%{n}-%{realversion}/cmake -GNinja \
   -DPYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3 \
   -DCMAKE_BUILD_TYPE=Release \
   -DCMAKE_INSTALL_PREFIX="%{i}" \
   -DCMAKE_INSTALL_LIBDIR=lib \
   -Donnxruntime_ENABLE_PYTHON=ON \
   -Donnxruntime_BUILD_SHARED_LIB=ON \
   -Donnxruntime_USE_CUDA=OFF \
   -Donnxruntime_BUILD_CSHARP=OFF \
   -Donnxruntime_USE_EIGEN_FOR_BLAS=ON \
   -Donnxruntime_USE_OPENBLAS=OFF \
   -Donnxruntime_USE_MKLML=OFF \
   -Donnxruntime_USE_NGRAPH=OFF \
   -Donnxruntime_USE_OPENMP=OFF \
   -Donnxruntime_USE_TVM=OFF \
   -Donnxruntime_USE_LLVM=OFF \
   -Donnxruntime_ENABLE_MICROSOFT_INTERNAL=OFF \
   -Donnxruntime_USE_BRAINSLICE=OFF \
   -Donnxruntime_USE_NUPHAR=OFF \
   -Donnxruntime_USE_TENSORRT=OFF \
   -Donnxruntime_CROSS_COMPILING=OFF \
   -Donnxruntime_USE_FULL_PROTOBUF=ON \
   -Donnxruntime_DISABLE_CONTRIB_OPS=OFF \
   -Donnxruntime_USE_PREINSTALLED_PROTOBUF=ON \
   -Donnxruntime_PREFER_SYSTEM_LIB=ON \
   -DCMAKE_PREFIX_PATH="${ZLIB_ROOT};${LIBPNG_ROOT};${PROTOBUF_ROOT};${PY2_PYBIND11_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)
python3 ../%{n}-%{realversion}/setup.py build

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
mkdir -p %{i}/${PYTHON3_LIB_SITE_PACKAGES}
mv build/lib/onnxruntime %{i}/${PYTHON3_LIB_SITE_PACKAGES}/
