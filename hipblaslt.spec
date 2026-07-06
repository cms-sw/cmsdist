## INCLUDE rocm-config
### RPM external hipblaslt %{rocm_version_num}
BuildRequires: rocm-cmake
Requires: rocm-hip rocm-core rocm-llvm rocr-runtime hipblas-common roctracer rocm-smi-lib msgpack-cxx boost google-test amdsmi rocm-comgr python3
%define cmake_args -DCMAKE_CXX_FLAGS="-I$ROCTRACER_ROOT/include" -DHIPBLASLT_ENABLE_DEVICE=off -DHIPBLASLT_ENABLE_CLIENT=off -DORIGAMI_BUILD_TESTING=off -DHIPBLASLT_ENABLE_ROCROLLER=OFF -DPython3_ROOT_DIR=$PYTHON3_ROOT
## INCLUDE rocm-libraries-build
