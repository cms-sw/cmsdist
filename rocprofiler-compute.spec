## INCLUDE rocm-config
### RPM external rocprofiler-compute %{rocm_version_num}
BuildRequires: cmake rocm-cmake
Requires: rocm-core rocm-llvm rocr-runtime python3 rocprofiler roctracer rocm-hip libxml2 rocm-rocprofiler-sdk elfutils
Requires: py3-astunparse py3-colorlover py3-kaleido py3-matplotlib
Requires: py3-numpy py3-pandas
Requires: py3-plotext py3-plotille py3-pymongo
Requires: py3-PyYAML py3-setuptools py3-sqlalchemy
Requires: py3-tabulate py3-textual py3-tqdm py3-textual-plotext py3-textual-fspicker
Requires: py3-dash-bootstrap-components py3-dash-svg py3-dash
%define ROCMPreBuild export PKG_CONFIG_PATH=${ELFUTILS_ROOT}/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}
%define cmake_args -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ -DBUILD_TESTING=OFF
%define ROCMPostInstall rm -fr %{i}/bin/roofline-rhel8-rocm6 %{i}/bin/roofline-sles15sp6-rocm6 %{i}/bin/roofline-ubuntu22_04-rocm6 %{i}/bin/roofline-azurelinux3-rocm7 %{i}/bin/roofline-sles15sp6-rocm7 %{i}/bin/roofline-ubuntu22_04-rocm7
%define ROCMPostPost %{relocateConfig}/share/rocprofiler-compute/modulefiles/rocprofiler-compute/*.lua
## INCLUDE rocm-systems-build
