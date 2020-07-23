### RPM external fmt 7.0.1

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
%ifarch ppc64le
    -DCMAKE_CXX_FLAGS="-mlong-double-64" \
%endif
    -DBUILD_SHARED_LIBS=TRUE

make %{makeprocesses}

%install

cd %{_builddir}/build
make install

