## INCLUDE rocm-config
### RPM external rocr-runtime %{rocm_version_num}

Source0: %{rocm_systems_source}/%{n}.tar.gz
Requires: rocm-core zlib libxml2 rocprofiler-register numactl rocm-llvm
%prep
%setup -q -n %{n}
%build
export PKG_CONFIG_PATH=/usr/lib64/pkgconfig
cmake \
  -S %{_builddir}/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/lib/llvm/bin/clang \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DLLVM_DIR=${ROCM_LLVM_ROOT}/lib/cmake/llvm \
  -DBUILD_SHARED_LIBS=ON \
  -DSO_VERSION_STRING=1.18.0 \
  -DClang_DIR=$ROCM_LLVM_ROOT/lib/llvm/lib/cmake/clang \
  -DCMAKE_C_FLAGS="-I${NUMACTL_ROOT}/include" \
  -DCMAKE_CXX_FLAGS="-I${NUMACTL_ROOT}/include"

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
