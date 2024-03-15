### RPM external tensorflow-xla-runtime 2.12.0
## INCLUDE cpp-standard

Requires: eigen py3-tensorflow
BuildRequires: cmake

%prep

cp -r ${PY3_TENSORFLOW_ROOT}/lib/python%{cms_python3_major_minor_version}/site-packages/tensorflow .

%build

export CPATH="${CPATH}:${EIGEN_ROOT}/include/eigen3"

%define cxxflags -fPIC
%ifarch x86_64
%define cxxflags -msse3 %{cxxflags}
%endif

pushd tensorflow/xla_aot_runtime_src
  cmake . -DCMAKE_CXX_FLAGS=%{cxxflags} -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} -DBUILD_SHARED_LIBS=OFF
  make %{makeprocesses}
popd

%install

mkdir -p %{i}/lib/archive
mv tensorflow/xla_aot_runtime_src/libtf_xla_runtime.a %{i}/lib/archive/libtf_xla_runtime-static.a
