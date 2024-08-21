### RPM external tensorflow-xla-runtime 2.12.0
## INCLUDE cpp-standard
## INCLUDE compilation_flags
## INCLUDE microarch_flags

Source99: scram-tools.file/tools/eigen/env

Patch0: tensorflow-xla-runtime

Requires: eigen py3-tensorflow abseil-cpp tensorflow
BuildRequires: cmake

%prep

cp -r ${PY3_TENSORFLOW_ROOT}/lib/python%{cms_python3_major_minor_version}/site-packages/tensorflow .
%patch0 -p0

%build

source %{_sourcedir}/env
export CPATH="${CPATH}:${EIGEN_ROOT}/include/eigen3"

CXXFLAGS="-fPIC -Wl,-z,defs %{arch_build_flags} ${CMS_EIGEN_CXX_FLAGS} %{selected_microarch}"

pushd tensorflow/xla_aot_runtime_src
  # remove unnecessary implementations that use symbols that are not even existing
  find . -type f -path '*/service/cpu/runtime_fork_join.cc' | xargs rm -f
  find . -type f -path '*/service/cpu/runtime_fft.cc' | xargs rm -f
  find . -type f -path '*/service/cpu/runtime_single_threaded_fft.cc' | xargs rm -f

  cmake . \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS}" \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DCMAKE_PREFIX_PATH=${ABSEIL_CPP_ROOT} \
    -DLIBFFT_WRAPPER=${TENSORFLOW_ROOT}/lib/libfft_wrapper.so \
    -DBUILD_SHARED_LIBS=ON
  make %{makeprocesses}
popd

%install

mkdir -p %{i}/lib
mv tensorflow/xla_aot_runtime_src/libtf_xla_runtime.so %{i}/lib/
