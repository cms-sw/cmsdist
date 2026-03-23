### RPM external rocm-rocprofiler 7.10

Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/rocprofiler.tar.gz
Source1: https://github.com/google/perfetto/archive/eb5ef24c58d13cec289d733d03f0f3f0ed321b12.tar.gz
Requires: rocm-core rocm-llvm hsa-rocr python3 rocm-cmake rocm-aqlprofile hip numactl libxml2 rocm-roctracer py3-lxml py3-barectf py3-PyYAML

%prep
%setup -q -n rocprofiler

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build
tar -xzf %{_sourcedir}/eb5ef24c58d13cec289d733d03f0f3f0ed321b12.tar.gz -C %{_builddir}/rocprofiler/plugin/perfetto/perfetto --strip-components=1
sed -i '1,7d' %{_builddir}/rocprofiler/plugin/perfetto/CMakeLists.txt #Downloads the submodule otherwise
#No otherway to turn off tests
sed -i \
  's/^set(ROCPROFILER_BUILD_TESTS ON)/set(ROCPROFILER_BUILD_TESTS OFF)/' \
  %{_builddir}/rocprofiler/CMakeLists.txt

sed -i \
  's/^set(ROCPROFILER_BUILD_CI ON)/set(ROCPROFILER_BUILD_CI OFF)/' \
  %{_builddir}/rocprofiler/CMakeLists.txt

#Needed by att_plugin
export CPATH="${GCC_ROOT}/include"

cmake \
  -S %{_builddir}/rocprofiler \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_FIND_DEBUG_MODE=ON \
  -DCMAKE_CXX_FLAGS="-I${NUMACTL_ROOT}/include -I${ROCM_CORE_ROOT}/include" \
  -DCMAKE_C_FLAGS="-I${NUMACTL_ROOT}/include -I${ROCM_CORE_ROOT}/include" \
  -DCMAKE_SHARED_LINKER_FLAGS="-L${GCC_ROOT}/lib -L${NUMACTL_ROOT}/lib" \
  -DCMAKE_EXE_LINKER_FLAGS="-L${GCC_ROOT}/lib -L${NUMACTL_ROOT}/lib" 

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
