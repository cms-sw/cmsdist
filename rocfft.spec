## INCLUDE rocm-config
### RPM external rocfft %{rocm_version}
Requires: hiprand rocm-llvm
Source0: %{rocm_libraries_source}%{n}.tar.gz
Requires: hip rocm-core rocm-llvm rocr-runtime rocm-cmake comgr
## INCLUDE rocm-flags

%prep
%setup -q -n %{n}

%build
#export LD_LIBRARY_PATH=$ROCR_RUNTIME_ROOT/lib:$ROCM_LLVM_ROOT/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export HIP_DEVICE_LIB_PATH=$ROCM_LLVM_ROOT/amdgcn/bitcode
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/%{n}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang++
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DBUILD_CLIENTS_TESTS=off
  -DGPU_TARGETS="%{rocm_archs}"
  -DROCFFT_BUILD_OFFLINE_TUNER=OFF
  -DROCFFT_KERNEL_CACHE_ENABLE=OFF
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
