### RPM external onnxruntime 1.20.1
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
## INCLUDE cuda-flags
%define github_user cms-externals
%define branch cms/v%{realversion}
%define tag efe7f6a3859bedbad40a2991480be4e7584b1582
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja
Requires: protobuf py3-numpy py3-wheel py3-onnx zlib libpng py3-pybind11 re2
%{!?without_cuda:Requires: cuda cudnn}

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build

USE_CUDA=OFF
if [ "%{cuda_gcc_support}" = "true" ] ; then
  USE_CUDA=ON
fi

cmake ../%{n}-%{realversion}/cmake -GNinja \
   -DPYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3 \
   -DCMAKE_BUILD_TYPE=Release \
   -DCMAKE_INSTALL_PREFIX="%{i}" \
   -DCMAKE_INSTALL_LIBDIR=lib \
   -Donnxruntime_ENABLE_PYTHON=ON \
   -Donnxruntime_BUILD_SHARED_LIB=ON \
   -Donnxruntime_USE_CUDA=${USE_CUDA} \
%if 0%{!?without_cuda:1}
   -Donnxruntime_CUDA_HOME="${CUDA_ROOT}" \
   -Donnxruntime_CUDNN_HOME="${CUDNN_ROOT}" \
   -Donnxruntime_NVCC_THREADS=0 \
   -DCMAKE_CUDA_ARCHITECTURES=$(echo %{cuda_arch} | tr ' ' ';' | sed 's|;;*|;|') \
   -DCMAKE_CUDA_FLAGS="-DTHRUST_IGNORE_DEPRECATED_API -DCUB_IGNORE_DEPRECATED_API -Wno-deprecated-gpu-targets --static-global-template-stub=false -cudart shared" \
   -DCMAKE_CUDA_RUNTIME_LIBRARY=Shared \
   -DCMAKE_TRY_COMPILE_PLATFORM_VARIABLES="CMAKE_CUDA_RUNTIME_LIBRARY" \
%endif
   -Donnxruntime_BUILD_CSHARP=OFF \
   -Donnxruntime_USE_OPENMP=OFF \
   -Donnxruntime_USE_TVM=OFF \
   -Donnxruntime_USE_LLVM=OFF \
   -Donnxruntime_ENABLE_MICROSOFT_INTERNAL=OFF \
   -Donnxruntime_USE_NUPHAR=OFF \
   -Donnxruntime_USE_TENSORRT=OFF \
   -Donnxruntime_CROSS_COMPILING=OFF \
   -Donnxruntime_USE_FULL_PROTOBUF=ON \
   -Donnxruntime_DISABLE_CONTRIB_OPS=OFF \
   -Donnxruntime_PREFER_SYSTEM_LIB=ON \
   -Donnxruntime_BUILD_UNIT_TESTS=OFF \
   -DCMAKE_PREFIX_PATH="${ZLIB_ROOT};${LIBPNG_ROOT};${PROTOBUF_ROOT};${PY3_PYBIND11_ROOT};${RE2_ROOT}" \
   -DRE2_INCLUDE_DIR="${RE2_ROOT}/include" \
   -DCMAKE_CXX_FLAGS="-Wno-error=stringop-overflow -Wno-error=maybe-uninitialized"

# -Wno-error=stringop-overflow is needed to work around a false positive string overflow,
# see https://github.com/google/flatbuffers/issues/7366

# -Wno-error=maybe-uninitialized is needed for ONNX runtime 1.17.1 with cuDNN 8.9 or 9.0

ninja -v %{makeprocesses}
python3 ../%{n}-%{realversion}/setup.py build

%install
cd ../build
ninja -v %{makeprocesses} install
mkdir -p %{i}/${PYTHON3_LIB_SITE_PACKAGES}
mv build/lib/onnxruntime %{i}/${PYTHON3_LIB_SITE_PACKAGES}/
