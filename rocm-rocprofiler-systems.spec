### RPM external rocm-rocprofiler-systems 7.10

Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/rocprofiler-systems.tar.gz

Requires: rocm-core rocm-llvm hsa-rocr cmake rocm-cmake rocm-rocprofiler roctracer hip libxml2
Requires: libunwind sqlite

%prep
%setup -q -n rocprofiler-systems

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/rocprofiler-systems \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DROCPROFSYS_BUILD_DYNINST=ON \
  -DROCPROFSYS_USE_LIBIBERTY=ON \
  -DBUILD_TESTING=OFF

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
