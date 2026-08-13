## INCLUDE rocm-flags
### RPM external hipsparselt %{rocm_version_num}
BuildRequires: py3-packaging rocm-cmake
Requires: origami hipsparse msgpack-cxx rocm-core rocm-smi-lib rocminfo roctracer rocr-runtime boost
Requires: py3-joblib py3-PyYAML py3-msgpack rocm-llvm rocm-comgr
Requires: zlib
%define ROCMExtraSources projects/hipblaslt shared/stinkytofu/src/conversion/rocisa
%define cmake_args -DGPU_TARGETS="gfx942" -DHIPBLASLT_ENABLE_THEROCK=ON -DHIPSPARSELT_ENABLE_CLIENT=OFF -DHIPSPARSELT_ENABLE_FORTRAN=OFF  -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include -I$ROCTRACER_ROOT/include" -DPython3_ROOT_DIR=$PYTHON3_ROOT
## INCLUDE rocm-libraries-build
