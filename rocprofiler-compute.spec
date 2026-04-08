## INCLUDE rocm-config
### RPM external rocprofiler-compute %{rocm_version_num}

Source0:  %{rocm_systems_source}/%{n}.tar.gz
Requires: rocm-core rocm-llvm rocr-runtime python3 cmake rocm-cmake rocprofiler roctracer hip libxml2 rocm-rocprofiler-sdk
Requires: py3-astunparse py3-colorlover py3-kaleido py3-matplotlib
Requires: py3-numpy py3-pandas py3-pandas
Requires: py3-plotext py3-plotille py3-pymongo
Requires: py3-PyYAML py3-setuptools py3-sqlalchemy
Requires: py3-tabulate py3-textual py3-tqdm py3-textual-plotext py3-textual-fspicker
Requires: py3-dash-bootstrap-components py3-dash-svg py3-dash

%prep
%setup -q -n %{n}

%build

cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/%{n} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DBUILD_TESTING=OFF

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install 
rm -fr %{i}/bin/roofline-rhel8-rocm6  %{i}/bin/roofline-sles15sp6-rocm6  %{i}/bin/roofline-ubuntu22_04-rocm6
rm -fr %{i}/bin/roofline-azurelinux3-rocm7 %{i}/bin/roofline-sles15sp6-rocm7 %{i}/bin/roofline-ubuntu22_04-rocm7
