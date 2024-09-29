### RPM external tensorflow-xla-runtime 2.17.0
## INCLUDE cpp-standard
## INCLUDE compilation_flags
## INCLUDE microarch_flags

Source99: scram-tools.file/tools/eigen/env
Patch0: tensorflow-xla-runtime-absl
Requires: eigen abseil-cpp tensorflow
BuildRequires: cmake

%prep
case ${TENSORFLOW_VERSION} in
  %{realversion}|%{realversion}-*) ;;
  * ) echo "ERROR: Mismatch %{n} (%{realversion}) and tensorflow (${TENSORFLOW_VERSION}) versions."
      echo "Please update %{n}.spec to use ${TENSORFLOW_VERSION} verison."
      exit 1
      ;;
esac

cp -r ${TENSORFLOW_ROOT}/xla-aot-runtime .
%patch -p1

%build

source %{_sourcedir}/env
export CPATH="${CPATH}:${EIGEN_ROOT}/include/eigen3"

CXXFLAGS="-fPIC -Wl,-z,defs %{arch_build_flags} ${CMS_EIGEN_CXX_FLAGS} %{selected_microarch}"

pushd xla-aot-runtime/src
  # remove unnecessary implementations that use symbols that are not even existing
  find . -type f -path '*/service/cpu/runtime_fork_join.cc' | xargs rm -f

  cmake . \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS} -I${TENSORFLOW_ROOT}/include" \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DCMAKE_PREFIX_PATH=${ABSEIL_CPP_ROOT} \
    -DCMAKE_SHARED_LINKER_FLAGS="-L../lib -Wl,--whole-archive -l:libfft_wrapper.pic.a -Wl,--no-whole-archive -l:libfft.pic.a -l:libmutex.pic.a -l:libnsync_cpp.pic.a" \
    -DBUILD_SHARED_LIBS=ON
  make %{makeprocesses}
popd

%install

mkdir -p %{i}/lib
mv xla-aot-runtime/src/libtf_xla_runtime.so %{i}/lib/
