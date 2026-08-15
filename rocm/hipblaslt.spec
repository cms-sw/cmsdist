## INCLUDE rocm/flags
### RPM external hipblaslt %{rocm_version_num}
BuildRequires: rocm-cmake
Requires: rocm-hip rocm-core rocm-llvm rocr-runtime rocm-smi-lib rocm-comgr
Requires: stinkytofu origami hipblas-common roctracer rocm-smi-lib msgpack-cxx boost amdsmi python3
%define ROCMExtraSources shared/stinkytofu/src/conversion/rocisa
%define cmake_args -DHIPBLASLT_ENABLE_THEROCK=ON -DCMAKE_CXX_FLAGS="-I$ROCTRACER_ROOT/include" -DHIPBLASLT_ENABLE_DEVICE=off -DHIPBLASLT_ENABLE_CLIENT=off -DHIPBLASLT_ENABLE_ROCROLLER=OFF -DPython3_ROOT_DIR=$PYTHON3_ROOT
## INCLUDE rocm/libraries-build
