### RPM external freetype 2.13.3
Source: http://download.savannah.gnu.org/releases/freetype/freetype-%{realversion}.tar.gz
Requires: bz2lib zlib libpng
BuildRequires: gmake cmake

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_BUILD_TYPE=Release \
  -DFT_REQUIRE_ZLIB=TRUE \
  -DFT_REQUIRE_BZIP2=TRUE \
  -DFT_REQUIRE_PNG=TRUE \
  -DCMAKE_PREFIX_PATH=%{cmake_prefix_path} \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_INSTALL_PREFIX="%{i}"

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install

%define strip_files %{i}/lib
%{relocateConfig}lib/cmake/freetype/freetype-config-release.cmake
%{relocateConfig}lib/cmake/freetype/freetype-config-version.cmake
%{relocateConfig}lib/cmake/freetype/freetype-config.cmake
%{relocateConfig}lib/pkgconfig/freetype2.pc
