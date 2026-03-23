### RPM external rocm-rocprofiler-compute 7.10

Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/rocprofiler-compute.tar.gz
Requires: rocm-core rocm-llvm hsa-rocr python3 cmake rocm-cmake rocm-rocprofiler rocm-roctracer hip libxml2
Requires: py3-astunparse py3-colorlover py3-kaleido py3-matplotlib
Requires: py3-numpy py3-pandas py3-pandas
Requires: py3-plotext py3-plotille py3-pymongo
Requires: py3-PyYAML py3-setuptools py3-sqlalchemy
Requires: py3-tabulate py3-textual py3-tqdm py3-textual-plotext py3-textual-fspicker
Requires: py3-dash-bootstrap-components py3-dash-svg py3-dash

%prep
%setup -q -n rocprofiler-compute

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/rocprofiler-compute \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install 
rm -fr %{i}/bin/roofline-rhel8-rocm6  %{i}/bin/roofline-sles15sp6-rocm6  %{i}/bin/roofline-ubuntu22_04-rocm6
rm -fr %{i}/bin/roofline-azurelinux3-rocm7 %{i}/bin/roofline-sles15sp6-rocm7 %{i}/bin/roofline-ubuntu22_04-rocm7
