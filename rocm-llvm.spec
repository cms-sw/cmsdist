## INCLUDE rocm-config
### RPM external rocm-llvm %{rocm_version_num}
## INITENV +PATH PATH %{i}/lib/llvm/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib/llvm/lib
## INITENV SET HIP_CLANG_PATH %{i}/lib/llvm/bin
## INCLUDE cpp-standard
%define keep_archives true

Source0: git+https://github.com/ROCm/llvm-project?obj=amd-staging/%{rocm_version}&export=%{n}-%{realversion}&output=/source.tar.gz
Source1: https://github.com/ROCm/rocm-systems/releases/download/%{rocm_version}/rocr-runtime.tar.gz
Requires: cmake ninja rocm-core rocm-cmake libxml2 zlib rocprofiler-register

%prep
%setup -q -n %{n}-%{realversion}

%build
tar -xzf %{_sourcedir}/rocr-runtime.tar.gz -C %{_builddir}

cp -rT %{_builddir}/rocr-runtime/runtime/hsa-runtime %{_builddir}/%{n}-%{realversion}/hsa-runtime

host_triple=$(gcc -dumpmachine)
cmake -G Ninja \
  -S %{_builddir}/%{n}-%{realversion}/llvm \
  -B %{_builddir}/build-llvm \
  -DCMAKE_INSTALL_PREFIX=%{i}/lib/llvm \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
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
  -DBUILD_TESTING=OFF \
  -DRUNTIMES_CMAKE_ARGS="-DLIBUNWIND_USE_COMPILER_RT=ON;-DCMAKE_PREFIX_PATH=%{cmake_prefix_path};-DLIBOMPTARGET_HSA_INCLUDE_DIRS=%{_builddir}/%{n}-%{realversion}/hsa-runtime/inc;-DLIBOMPTARGET_NO_SANITIZER_AMDGPU=ON;-DOFFLOAD_EXTERNAL_PROJECT_UNIFIED_ROCR=OFF"

echo -e "--gcc-toolchain=$GCC_ROOT\n--target=$host_triple\n-m64\n-L$GCC_ROOT/lib64" > %{_builddir}/build-llvm/bin/clang++.cfg
ln -sf %{_builddir}/build-llvm/bin/clang++.cfg %{_builddir}/build-llvm/bin/clang.cfg
ln -sf %{_builddir}/build-llvm/bin/clang++.cfg %{_builddir}/build-llvm/bin/$host_triple.cfg

ninja -C %{_builddir}/build-llvm %{makeprocesses}

cmake -G Ninja \
  -S %{_builddir}/%{n}-%{realversion}/amd/device-libs \
  -B %{_builddir}/build-device-libs \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_C_COMPILER=%{_builddir}/build-llvm/bin/clang \
  -DCMAKE_CXX_COMPILER=%{_builddir}/build-llvm/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_PREFIX_PATH="%{_builddir}/build-llvm;%{cmake_prefix_path}"
ninja -C %{_builddir}/build-device-libs %{makeprocesses}

cmake -G Ninja \
  -S  %{_builddir}/%{n}-%{realversion}/amd/comgr \
  -B %{_builddir}/build-comgr \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_C_COMPILER=%{_builddir}/build-llvm/bin/clang \
  -DCMAKE_CXX_COMPILER=%{_builddir}/build-llvm/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DBUILD_TESTING=OFF \
  -DCMAKE_PREFIX_PATH="%{_builddir}/build-llvm;%{_builddir}/build-device-libs;%{cmake_prefix_path}"
ninja -C %{_builddir}/build-comgr %{makeprocesses}

cmake -G Ninja \
  -S  %{_builddir}/%{n}-%{realversion}/amd/hipcc \
  -B %{_builddir}/build-hip \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_C_COMPILER=%{_builddir}/build-llvm/bin/clang \
  -DCMAKE_CXX_COMPILER=%{_builddir}/build-llvm/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{_builddir}/build-llvm;%{cmake_prefix_path}"
ninja  -C %{_builddir}/build-hip  %{makeprocesses}

%install
ninja -C %{_builddir}/build-llvm %{makeprocesses} install
ninja -C %{_builddir}/build-llvm/runtimes/runtimes-bins %{makeprocesses} install
ninja -C %{_builddir}/build-llvm/runtimes/builtins-bins %{makeprocesses} install
ninja -C %{_builddir}/build-device-libs install
ninja -C %{_builddir}/build-comgr install
ninja -C %{_builddir}/build-hip install

mkdir -p %{i}/lib/llvm/bin/
mv  %{_builddir}/build-llvm/bin/clang++.cfg %{i}/lib/llvm/bin/

ln -r -s -f %{i}/lib/llvm/bin/amdclang     %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdclang++   %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdclang-cl  %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdclang-cpp %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdflang     %{i}/bin/
ln -r -s -f %{i}/lib/llvm/bin/amdlld       %{i}/bin/

%post
%if 0%{!?use_system_gcc:1}
%{relocateConfig}/llvm/bin/clang++.cfg
%endif
