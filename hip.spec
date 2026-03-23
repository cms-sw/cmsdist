### RPM external hip 7.10
## INCLUDE cpp-standard
Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/clr.tar.gz
Source1: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/hip.tar.gz
BuildRequires: rocm-llvm rocm-cmake rocm-core rocm-info hsa-rocr rocprofiler-register numactl
Requires: rocm-llvm rocm-core hsa-rocr rocprofiler-register numactl py3-CppHeaderParser python3
Provides: perl(URI::Escape)
%prep
%setup -q -n clr
cd %{_builddir}
tar xf %{SOURCE1}
%build
mkdir -p %{_builddir}/build-hip
cd %{_builddir}/build-hip
cmake \
  -S %{_builddir}/clr \
  -DHIP_COMMON_DIR=%{_builddir}/hip \
  -DHIP_PLATFORM=amd \
  -DCLR_BUILD_HIP=ON \
  -DCLR_BUILD_OCL=OFF \
  -DHIP_INSTALLS_HIPCC=ON \
  -DHIPCC_BIN_DIR=${ROCM_LLVM_ROOT}/bin \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DHSA_PATH=${HSA_ROCR_ROOT} \
  -DROCM_PATH=${ROCM_LLVM_ROOT} \
  -DDEVICE_LIB_PATH=${ROCM_LLVM_ROOT}/amdgcn/bitcode
make %{makeprocesses}
%install
make -C %{_builddir}/build-hip %{makeprocesses} install
