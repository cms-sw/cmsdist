## INCLUDE rocm-config
### RPM external miopen %{rocm_version}
Source0: https://github.com/ROCm/rocm-libraries/archive/refs/tags/%{rocm_version}.tar.gz
Source1: https://raw.githubusercontent.com/suruoxi/half/refs/heads/master/include/half.hpp
Requires: hip rocm-core rocm-cmake rocr-runtime rocminfo python3 roctracer sqlite hipblaslt hipblas rocblas rocrand bz2lib hipblas
Requires: json hipblas-common boost zstd google-test opencl rocm-llvm

%prep
%setup -q -n rocm-libraries-%{realversion}
cp %{_sourcedir}/half.hpp %{_builddir}

%build
mkdir -p %{_builddir}/half-include/half
cp %{_sourcedir}/half.hpp %{_builddir}/half-include/half/

CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/rocm-libraries-%{realversion}/projects/%{n}
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DGPU_TARGETS="gfx908;gfx90a;gfx942;gfx1030;gfx1100;gfx1102"
  -DCK_USE_ALTERNATIVE_PYTHON=$PYTHON3_ROOT/bin/python3
  -DMIOPEN_USE_COMPOSABLEKERNEL=OFF
  -DMIOPEN_USE_MLIR=OFF
  -DMIOPEN_USE_COMGR=ON
  -DBoost_USE_STATIC_LIBS=OFF
  -DMIOPEN_ENABLE_AI_KERNEL_TUNING=OFF
  -DMIOPEN_ENABLE_AI_IMMED_MODE_FALLBACK=OFF
  -DMIOPEN_BACKEND=HIP
  -DMIOPEN_BUILD_DRIVER=OFF
  -DHALF_INCLUDE_DIR=%{_builddir}/half-include
  -DBUILD_TESTING=OFF
)
sed -i '827,830d' %{_builddir}/rocm-libraries-%{realversion}/projects/%{n}/CMakeLists.txt
cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
