### RPM external abseil-cpp 20230125.3
## INCLUDE cpp-standard

Source: https://github.com/abseil/abseil-cpp/archive/%{realversion}.tar.gz
Source2: https://patch-diff.githubusercontent.com/raw/abseil/abseil-cpp/pull/1732.diff
BuildRequires: cmake gmake

%prep
%setup -n %{n}-%{realversion}
patch -p1 <%{_sourcedir}/1732.diff

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DBUILD_TESTING=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Release

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install

%define strip_files %i/lib
%define drop_files %i/lib/pkgconfig
