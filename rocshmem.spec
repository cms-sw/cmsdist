## INCLUDE rocm-config
### RPM external rocshmem %{rocm_version_num}
BuildRequires: rocm-cmake
Requires: rocm-core rocm-llvm rocr-runtime rocm-hip
Requires: openmpi rocm-comgr
%define cmake_args -DCMAKE_PREFIX_PATH="%{cmake_prefix_path};$ROCM_CMAKE_ROOT" -DROCM_PATH=$ROCM_LLVM_ROOT -DUSE_EXTERNAL_MPI=ON -DBUILD_TESTING=OFF -DCMAKE_CXX_FLAGS="-I$ROCM_CORE_ROOT/include --rocm-device-lib-path=${ROCM_LLVM_ROOT}/amdgcn/bitcode" -DEXPLICIT_ROCM_VERSION=%{rocm_version_num}.0
## INCLUDE rocm-systems-build
