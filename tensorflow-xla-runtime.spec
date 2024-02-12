### RPM external tensorflow-xla-runtime 2.12.0

Requires: eigen tensorflow-sources
BuildRequires: cmake

%prep
unzip -q -o ${TENSORFLOW_SOURCES_ROOT}/tensorflow-%{realversion}-cp%{cms_python3_major_minor}-cp%{cms_python3_major_minor}-linux_%{_arch}.whl

%build

# fix a single comparison between size_t and int
sed -i -r 's/assert\(\(arg_size\(index\)/assert\(\(\(size_t\)arg_size\(index\)/' tensorflow/include/tensorflow/compiler/tf2xla/xla_compiled_cpu_function.h

export CPATH="${CPATH}:${EIGEN_ROOT}/include/eigen3"
export CPATH="${CPATH}:%{i}/tensorflow/include"
export CPATH="${CPATH}:%{i}/tensorflow/include/third_party/eigen3"

pushd tensorflow/xla_aot_runtime_src
  cmake . -DCMAKE_CXX_FLAGS="-fPIC -msse3"
  make %{makeprocesses}
  # this builds a shared library, but when used some symbols are missig (e.g `tsl::mutex::unlock()')
  # so it does not seem intended to be used as a shared lib
  gcc -shared -o libtf_xla_runtime.so -Wl,--whole-archive libtf_xla_runtime.a -Wl,--no-whole-archive
popd

%install

mv tensorflow/include %{i}

mkdir -p %{i}/lib/archive
mv tensorflow/xla_aot_runtime_src/libtf_xla_runtime.a %{i}/lib/archive/libtf_xla_runtime-static.a
mv tensorflow/xla_aot_runtime_src/libtf_xla_runtime.so %{i}/lib/libtf_xla_runtime.so
