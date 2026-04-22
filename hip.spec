## INCLUDE rocm-config
### RPM external hip %{rocm_version_num}
## INCLUDE cpp-standard
## INITENV SET HIP_PATH %{i}
## INITENV SET HIP_CLANG_PATH ${ROCM_LLVM_ROOT}/lib/llvm/bin
## INITENV HIP_PLATFORM amd
Source0: https://github.com/ROCm/rocm-systems/archive/refs/tags/rocm-%{realversion}.tar.gz
Requires: rocm-llvm rocm-core rocr-runtime rocprofiler-register numactl py3-CppHeaderParser python3
Provides: perl(URI::Escape)
%prep
%setup -q -n rocm-systems-rocm-%{realversion}
%build
mkdir -p %{_builddir}/build-hip
cd %{_builddir}/build-hip
cmake \
  -S %{_builddir}/rocm-systems-rocm-%{realversion}/projects/clr \
  -B %{_builddir}/build-hip \
  -DHIP_COMMON_DIR=%{_builddir}/rocm-systems-rocm-%{realversion}/projects/hip \
  -DHIP_PLATFORM=amd \
  -DCLR_BUILD_HIP=ON \
  -DCLR_BUILD_OCL=OFF \
  -DHIP_INSTALLS_HIPCC=ON \
  -DHIPCC_BIN_DIR=${ROCM_LLVM_ROOT}/bin \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DHSA_PATH=${HSA_ROCR_ROOT} \
  -DROCM_PATH=${ROCM_LLVM_ROOT} \
  -DDEVICE_LIB_PATH=${ROCM_LLVM_ROOT}/amdgcn/bitcode \
  -DLLVM_DIR=${ROCM_LLVM_ROOT}/lib/llvm/lib/cmake/llvm
make %{makeprocesses}
%install
make -C %{_builddir}/build-hip %{makeprocesses} install
