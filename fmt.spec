### RPM external fmt 11.0.1
## INCLUDE compilation_flags
Source: https://github.com/fmtlib/fmt/archive/%{realversion}.tar.gz
BuildRequires: gmake cmake

%prep
%setup -n %{n}-%{realversion}

%build

cd %{_builddir}
rm -rf build && mkdir build && cd build

cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX:STRING=%{i} \
    -DCMAKE_INSTALL_LIBDIR:STRING=lib \
%if "%{?arch_build_flags}"
    -DCMAKE_CXX_FLAGS="%{arch_build_flags}" \
%endif
    -DBUILD_SHARED_LIBS=TRUE

make %{makeprocesses}

%install

cd %{_builddir}/build
make install

