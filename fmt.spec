### RPM external fmt 6.2.1

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
    -DBUILD_SHARED_LIBS=TRUE

make %{makeprocesses}

%install

cd %{_builddir}/build
make install

