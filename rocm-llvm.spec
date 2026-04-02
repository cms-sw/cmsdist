## INCLUDE rocm-config
### RPM external rocm-llvm %{rocm_version_num}
## INCLUDE cpp-standard
%define keep_archives true

Source0: https://github.com/ROCm/llvm-project/archive/refs/tags/%{rocm_version}.tar.gz
Source1: https://github.com/ROCm/rocm-systems/releases/download/%{rocm_version}/rocr-runtime.tar.gz
Requires: cmake ninja rocm-core rocm-cmake libxml2 zlib rocprofiler-register

%prep
%setup -q -n llvm-project-%{rocm_version}

%build
tar -xzf %{_sourcedir}/rocr-runtime.tar.gz -C %{_builddir}
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cp -rT %{_builddir}/rocr-runtime/runtime/hsa-runtime %{_builddir}/llvm-project-%{rocm_version}/hsa-runtime

host_triple=$(gcc -dumpmachine)

cmake -G Ninja \
  -S %{_builddir}/llvm-project-%{rocm_version}/llvm \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DLLVM_TARGETS_TO_BUILD="AMDGPU;X86" \
  -DLLVM_ENABLE_PROJECTS="clang;lld;clang-tools-extra" \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt;libunwind;libcxxabi;libcxx;openmp" \
  -DLLVM_ENABLE_ZLIB=ON \
  -DLLVM_ENABLE_RTTI=ON \
  -DLLVM_INSTALL_UTILS=ON \
  -DLLVM_ENABLE_PIC=ON \
  -DLLVM_INSTALL_STATIC_LIBS=ON \
  -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
  -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
  -DLLVM_DYLIB_EXPORT_ALL=ON \
  -DPACKAGE_VENDOR=AMD \
  -DCLANG_DEFAULT_LINKER=lld \
  -DCLANG_ENABLE_AMDCLANG=ON \
  -DCLANG_DEFAULT_PIE_ON_LINUX=OFF \
  -DLLVM_HOST_TRIPLE=$host_triple \
  -DLLVM_EXTERNAL_PROJECTS="device-libs;comgr;hipcc" \
  -DLLVM_EXTERNAL_DEVICE_LIBS_SOURCE_DIR=%{_builddir}/llvm-project-rocm-%{realversion}/amd/device-libs \
  -DLLVM_EXTERNAL_COMGR_SOURCE_DIR=%{_builddir}/llvm-project-rocm-%{realversion}/amd/comgr \
  -DLLVM_EXTERNAL_HIPCC_SOURCE_DIR=%{_builddir}/llvm-project-rocm-%{realversion}/amd/hipcc \
  -DBUILD_TESTING=OFF \
  -DRUNTIMES_CMAKE_ARGS="-DLIBUNWIND_USE_COMPILER_RT=ON;-DCMAKE_PREFIX_PATH=%{cmake_prefix_path};-DLIBOMPTARGET_HSA_INCLUDE_DIRS=%{_builddir}/llvm-project-rocm-%{realversion}/hsa-runtime/inc;-DLIBOMPTARGET_NO_SANITIZER_AMDGPU=ON;-DOFFLOAD_EXTERNAL_PROJECT_UNIFIED_ROCR=OFF"

echo -e "--gcc-toolchain=$GCC_ROOT\n--target=$host_triple\n-m64" > bin/clang++.cfg
ln -sf clang++.cfg bin/clang.cfg

ninja %{makeprocesses} clang-offload-bundler clang lld
ninja %{makeprocesses}
%install
ninja -C %{_builddir}/build %{makeprocesses} install
ninja -C %{_builddir}/build/runtimes/runtimes-bins %{makeprocesses} install
ninja -C %{_builddir}/build/runtimes/builtins-bins  %{makeprocesses} install

mv %{_builddir}/build/bin/clang++.cfg %{i}/bin
mv %{_builddir}/build/bin/clang.cfg %{i}/bin
