## INCLUDE rocm-config
### RPM external comgr %{rocm_version_num}
Source0: https://github.com/ROCm/llvm-project/archive/refs/tags/rocm-%{realversion}.tar.gz
Requires: rocm-llvm rocm-core zlib zstd cmake ninja libxml2
Patch0: 0001-comgr-link-with-static-llvm

%prep
%setup -q -n llvm-project-rocm-%{realversion}
%patch0 -p1

%build

sed -i "s/TARGET clangFrontendTool/true/" %{_builddir}/llvm-project-rocm-%{realversion}/amd/comgr/CMakeLists.txt

cmake -G "Unix Makefiles" \
  -S  %{_builddir}/llvm-project-rocm-%{realversion}/amd/comgr \
  -B %{_builddir}/build-comgr \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/lib/llvm/bin/clang \
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/lib/llvm/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DCOMGR_BUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCOMGR_STATIC_LLVM=ON \
  -DBUILD_TESTING=OFF \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" 

sed -i -e 's@libLLVM.so.22.0git@libLLVMCore.a@' %{_builddir}/build-comgr/CMakeFiles/amd_comgr.dir/link.txt
sed -i -e "s@-lrt -lpthread -lm@-L$ROCM_LLVM_ROOT/lib/llvm/lib/ -lLLVMCoverage -lLLVMFrontendDriver -lLLVMFrontendHLSL -lLLVMLTO -lLLVMOption -lLLVMSymbolize -lLLVMWindowsDriver -lrt -lpthread -lm@" %{_builddir}/build-comgr/CMakeFiles/amd_comgr.dir/link.txt

make -C %{_builddir}/build-comgr %{makeprocesses}
%install
make -C %{_builddir}/build-comgr install
