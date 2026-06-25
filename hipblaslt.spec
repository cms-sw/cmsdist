## INCLUDE rocm-config
### RPM external hipblaslt %{rocm_version_num}
Requires: hip rocm-core rocm-llvm rocr-runtime rocm-cmake hipblas-common roctracer rocm-smi-lib msgpack-cxx boost google-test amdsmi comgr python3
%define cmake_args -DCMAKE_CXX_FLAGS="-I$ROCTRACER_ROOT/include" -DHIPBLASLT_ENABLE_DEVICE=off -DHIPBLASLT_ENABLE_CLIENT=off -DORIGAMI_BUILD_TESTING=off -DHIPBLASLT_ENABLE_ROCROLLER=OFF -DPython3_ROOT_DIR=$PYTHON3_ROOT
## INCLUDE rocm-libraries-build
