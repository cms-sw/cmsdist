### RPM external libyaml 0.2.5
%define keep_archives true
Source: https://github.com/yaml/libyaml/archive/refs/tags/%{realversion}.tar.gz
BuildRequires: cmake gmake

%prep
%setup -n %{n}-%{realversion}

%build
cmake -B %{_builddir}/build \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DCMAKE_INSTALL_PREFIX=%{i}

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install VERBOSE=1
