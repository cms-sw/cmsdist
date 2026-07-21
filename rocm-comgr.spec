## INCLUDE rocm-config
### RPM external rocm-comgr %{rocm_version_num}
Source0: https://github.com/ROCm/llvm-project/archive/refs/tags/therock-%{realversion}.tar.gz
BuildRequires: cmake ninja
Requires: rocm-llvm rocm-core zlib zstd libxml2

%prep
%setup -q -n llvm-project-therock-%{rocm_version_num}

%build

grep -q 'if(NOT CLANG_LINK_CLANG_DYLIB)' %{_builddir}/llvm-project-therock-%{rocm_version_num}/amd/comgr/CMakeLists.txt
sed -i 's/if(NOT CLANG_LINK_CLANG_DYLIB)/if(TRUE)/' %{_builddir}/llvm-project-therock-%{rocm_version_num}/amd/comgr/CMakeLists.txt
grep -q '^\s*TargetParser\s*$' %{_builddir}/llvm-project-therock-%{rocm_version_num}/amd/comgr/CMakeLists.txt
sed -i -e 's|^\s*TargetParser\s*$| TargetParser Coverage FrontendDriver FrontendHLSL LTO Option Symbolize WindowsDriver|' %{_builddir}/llvm-project-therock-%{rocm_version_num}/amd/comgr/CMakeLists.txt

cmake -G "Unix Makefiles" \
  -S %{_builddir}/llvm-project-therock-%{rocm_version_num}/amd/comgr \
  -B %{_builddir}/build-comgr \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/lib/llvm/bin/clang \
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/lib/llvm/bin/clang++ \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCOMGR_BUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCOMGR_STATIC_LLVM=ON \
  -DBUILD_TESTING=OFF \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

LLVMLIBS="-L$ROCM_LLVM_ROOT/lib/llvm/lib $($ROCM_LLVM_ROOT/lib/llvm/bin/llvm-config --link-static --libs)"
grep -q -E ' [^ ]*libLLVM\.so(\.[0-9]+)+git( |$)' %{_builddir}/build-comgr/CMakeFiles/amd_comgr.dir/link.txt
sed -E -i \
  -e "s@[^ ]*libLLVM\.so(\.[0-9]+)+git@$LLVMLIBS@" \
  %{_builddir}/build-comgr/CMakeFiles/amd_comgr.dir/link.txt


make -C %{_builddir}/build-comgr %{makeprocesses} VERBOSE=1
%install
make -C %{_builddir}/build-comgr install VERBOSE=1
