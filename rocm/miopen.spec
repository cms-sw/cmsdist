## INCLUDE rocm/flags
### RPM external miopen %{rocm_version_num}
Source99: https://raw.githubusercontent.com/suruoxi/half/7cd91f2a3b5feba92a0eb44ed314e0ddb9962d89/include/half.hpp
Patch0: patches/miopen-boost-optional-fix
Patch1: patches/miopen-ciso646
BuildRequires: rocm-cmake
Requires: rocm-hip rocm-core rocr-runtime rocminfo python3 roctracer sqlite hipblaslt hipblas rocblas rocrand bz2lib
Requires: google-test eigen json hipblas-common boost zstd opencl rocm-llvm rocm-comgr

%define ROCMPostPrep patch -p2 -i %{PATCH0}; patch -p1 -i %{PATCH1}; mkdir -p %{_builddir}/half-include/half; cp %{_sourcedir}/half.hpp %{_builddir}/half-include/half
%define ROCMPostPost %{relocateConfig}/include/miopen/config.h
%define cmake_args -DCK_USE_ALTERNATIVE_PYTHON=$PYTHON3_ROOT/bin/python3 -DMIOPEN_USE_COMPOSABLEKERNEL=OFF -DMIOPEN_USE_MLIR=OFF -DMIOPEN_USE_COMGR=ON -DBoost_USE_STATIC_LIBS=OFF -DMIOPEN_ENABLE_AI_KERNEL_TUNING=OFF -DMIOPEN_ENABLE_AI_IMMED_MODE_FALLBACK=OFF -DMIOPEN_BACKEND=HIP -DMIOPEN_BUILD_DRIVER=OFF -DHALF_INCLUDE_DIR=%{_builddir}/half-include -DBUILD_TESTING=OFF

## INCLUDE rocm/libraries-build
