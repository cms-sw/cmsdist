## INCLUDE rocm-config
### RPM external miopen %{rocm_version_num}
Source1: https://raw.githubusercontent.com/suruoxi/half/refs/heads/master/include/half.hpp
Patch0: miopen-boost-optional-fix
BuildRequires: rocm-cmake
Requires: rocm-hip rocm-core rocr-runtime rocminfo python3 roctracer sqlite hipblaslt hipblas rocblas rocrand bz2lib hipblas
Requires: json hipblas-common boost zstd opencl rocm-llvm rocm-comgr

%define ROCMPrePrep cp %{_sourcedir}/half.hpp %{_builddir}
%define ROCMPostPrep %patch0 -p2
%define ROCMPreBuild mkdir -p %{_builddir}/half-include/half && cp %{_sourcedir}/half.hpp %{_builddir}/half-include/half/
%define ROCMPreCMake printf 'macro(enable_clang_tidy)\\nendmacro()\\nmacro(clang_tidy_check)\\nendmacro()\\n' > %{_builddir}/rocm-libraries/projects/%{n}/cmake/ClangTidy.cmake
%define ROCMPostCMake sed -i '827,830d' %{_builddir}/rocm-libraries/projects/%{n}/CMakeLists.txt
%define ROCMPostPost %{relocateConfig}/include/miopen/config.h
%define cmake_args -DCK_USE_ALTERNATIVE_PYTHON=$PYTHON3_ROOT/bin/python3 -DMIOPEN_USE_COMPOSABLEKERNEL=OFF -DMIOPEN_USE_MLIR=OFF -DMIOPEN_USE_COMGR=ON -DBoost_USE_STATIC_LIBS=OFF -DMIOPEN_ENABLE_AI_KERNEL_TUNING=OFF -DMIOPEN_ENABLE_AI_IMMED_MODE_FALLBACK=OFF -DMIOPEN_BACKEND=HIP -DMIOPEN_BUILD_DRIVER=OFF -DHALF_INCLUDE_DIR=%{_builddir}/half-include -DBUILD_TESTING=OFF

## INCLUDE rocm-libraries-build

