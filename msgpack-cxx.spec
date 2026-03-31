### RPM external msgpack-cxx 7.0.0
## INCLUDE cpp-standard
Source0: https://github.com/msgpack/msgpack-c/releases/download/cpp-%{realversion}/msgpack-cxx-%{realversion}.tar.gz
Requires: boost
%prep
%setup -q -n %{n}-%{realversion}
%build
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/%{n}-%{realversion}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DCMAKE_CXX_STANDARD="%{cms_cxx_standard}"
  -DMSGPACK_BUILD_DOCS=off
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
