## INCLUDE rocm/flags
### RPM external rocm-comgr %{rocm_version_num}
Source0: https://github.com/ROCm/llvm-project/archive/refs/tags/therock-%{realversion}.tar.gz
BuildRequires: cmake ninja
Requires: rocm-llvm rocm-core zlib zstd libxml2

%prep
%setup -q -n llvm-project-therock-%{rocm_version_num}

%build

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

make -C %{_builddir}/build-comgr %{makeprocesses} VERBOSE=1
%install
make -C %{_builddir}/build-comgr install VERBOSE=1
