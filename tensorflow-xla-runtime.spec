### RPM external tensorflow-xla-runtime 2.12.0
## INCLUDE cpp-standard
## INCLUDE compilation_flags

Source99: scram-tools.file/tools/eigen/env

Patch0: tensorflow-xla-runtime-absl

Requires: eigen py3-tensorflow abseil-cpp
BuildRequires: cmake

%prep

cp -r ${PY3_TENSORFLOW_ROOT}/lib/python%{cms_python3_major_minor_version}/site-packages/tensorflow .
%patch -p0

%build

source %{_sourcedir}/env
export CPATH="${CPATH}:${EIGEN_ROOT}/include/eigen3"

CXXFLAGS="-fPIC %{arch_build_flags} ${CMS_EIGEN_CXX_FLAGS}"
%ifarch x86_64
  CXXFLAGS="${CXXFLAGS} -msse3"
%endif

pushd tensorflow/xla_aot_runtime_src
  cmake . \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS}" \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DCMAKE_PREFIX_PATH=${ABSEIL_CPP_ROOT} \
    -DBUILD_SHARED_LIBS=ON
  make %{makeprocesses}
popd

%install

mkdir -p %{i}/lib
mv tensorflow/xla_aot_runtime_src/libtf_xla_runtime.so %{i}/lib/
