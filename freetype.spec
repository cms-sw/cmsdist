### RPM external freetype 2-14-3
Source: https://github.com/freetype/freetype/archive/refs/tags/VER-%{realversion}.tar.gz
Requires: bz2lib zlib libpng
BuildRequires: gmake cmake

%prep
%setup -n %{n}-VER-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-VER-%{realversion} \
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
