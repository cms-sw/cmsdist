## INCLUDE rocm/flags
### RPM external migraphx %{rocm_version_num}
## INCLUDE cpp-standard
# MIGraphX is not part of the rocm-libraries/rocm-systems monorepos, it is built from its own repository
Source: https://github.com/ROCm/AMDMIGraphX/archive/refs/tags/rocm-%{rocm_version_num}.tar.gz
# rocm_add_version_resource() is missing from the rocm-cmake in TheRock 7.14
Patch0: patches/migraphx-rocm-add-version-resource
# std::accumulate passes the accumulator as an rvalue in C++20
Patch1: patches/migraphx-cxx20-accumulate
# fix building without hipBLASLt (MIGRAPHX_USE_HIPBLASLT=OFF)
Patch2: patches/migraphx-without-hipblaslt
# fix building without rocMLIR (MIGRAPHX_ENABLE_MLIR=OFF): add the missing stubs
Patch3: patches/migraphx-without-mlir
BuildRequires: cmake rocm-cmake
Requires: rocm-hip rocm-core rocm-llvm rocr-runtime rocm-comgr
Requires: miopen rocblas
Requires: protobuf abseil-cpp json msgpack-cxx sqlite eigen boost zlib

%prep
%setup -q -n AMDMIGraphX-rocm-%{rocm_version_num}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# MIGraphX hardcodes -std=c++17, use the same C++ standard as the other CMSSW externals (e.g. abseil);
# -fno-cxx-modules (see below) is needed because MIGraphX uses "module" as a type name at the start of a line,
# which C++20 would parse as a module declaration
sed -i -e 's|-std=c++17>|-std=c++%{cms_cxx_standard}>|' CMakeLists.txt

%build
export HIP_DEVICE_LIB_PATH=${ROCM_LLVM_ROOT}/amdgcn/bitcode

# Optional components that are not (yet) available in CMSDIST are disabled:
#   - rocMLIR (MIGRAPHX_ENABLE_MLIR): MLIR-generated fused GEMM/convolution kernels
#   - composable_kernel (MIGRAPHX_USE_COMPOSABLEKERNEL): CK JIT GEMM kernels
#   - AMD MLSS (MIGRAPHX_USE_AMDMLSS)
# GEMMs and convolutions use rocBLAS and MIOpen instead.
# hipBLASLt is disabled because the CMSDIST hipblaslt is built without device kernels
# (HIPBLASLT_ENABLE_DEVICE=off), and MIGraphX would use it by default for GEMMs on gfx942.
# Pass -DROCM_ENABLE_CLANG_TIDY=OFF to avoid running into "File name too long" build errors.
cmake \
  -S %{_builddir}/AMDMIGraphX-rocm-%{rocm_version_num} \
  -B %{_builddir}/build \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  -DCMAKE_CXX_FLAGS="-fno-cxx-modules" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path};${ROCM_CMAKE_ROOT}" \
  -DHIP_ROOT=${ROCM_HIP_ROOT} \
  -DGPU_TARGETS="%{rocm_targets}" \
  -DBUILD_TESTING=OFF \
  -DROCM_ENABLE_CLANG_TIDY=OFF \
  -DMIGRAPHX_ENABLE_PYTHON=OFF \
  -DMIGRAPHX_ENABLE_MLIR=OFF \
  -DMIGRAPHX_USE_COMPOSABLEKERNEL=OFF \
  -DMIGRAPHX_USE_AMDMLSS=OFF \
  -DMIGRAPHX_USE_MIOPEN=ON \
  -DMIGRAPHX_USE_ROCBLAS=ON \
  -DMIGRAPHX_USE_HIPBLASLT=OFF

cmake --build %{_builddir}/build --parallel %{compiling_processes} --verbose

%install
cmake --install %{_builddir}/build --verbose
