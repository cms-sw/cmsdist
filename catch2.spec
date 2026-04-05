### RPM external catch2 3.13.0

Source: https://github.com/catchorg/Catch2/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: cmake gmake

%prep
%setup -n Catch2-%{realversion}

%build
cd %{_builddir}
rm -rf build && mkdir build && cd build

cmake ../Catch2-%{realversion} \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCATCH_INSTALL_HELPERS=ON \
  -DCATCH_INSTALL_EXTRAS=ON \
  -DCMAKE_INSTALL_COMPONENT="devel"

make %{makeprocesses} VERBOSE=1

%install
cd %{_builddir}/build
make install

%post
%{relocateConfig}share/pkgconfig/catch2*.pc
