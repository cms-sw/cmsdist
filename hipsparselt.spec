## INCLUDE rocm-config
### RPM external hipsparselt %{rocm_version_num}
Requires: hipsparse msgpack-cxx rocm-core rocm-smi-lib rocminfo roctracer rocr-runtime rocm-cmake boost
Requires: py3-joblib py3-PyYAML py3-msgpack py3-packaging rocm-llvm python3 comgr
%define cmake_args -DGPU_TARGETS="gfx942" -DHIPSPARSELT_ENABLE_CLIENT=OFF -DHIPSPARSELT_ENABLE_FORTRAN=OFF  -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include -I$ROCTRACER_ROOT/include"
## INCLUDE rocm-libraries-build
