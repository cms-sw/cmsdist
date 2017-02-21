### RPM external libtiff 4.0.3
Source: http://download.osgeo.org/libtiff/tiff-%{realversion}.zip

Requires: libjpeg-turbo zlib

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11 -O2
%endif

%prep
%setup -n tiff-%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

%build
./configure --prefix=%{i} --disable-static \
            --with-zlib-lib-dir=${ZLIB_ROOT}/lib \
            --with-zlib-include-dir=${ZLIB_ROOT}/include \
            --with-jpeg-lib-dir=${LIBJPEG_TURBO_ROOT}/lib \
            --with-jpeg-include-dir=${LIBJPEG_TURBO_ROOT}/include \
            --disable-dependency-tracking \
            --without-x \
            CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags"
                          
make %{makeprocesses}

%install
make install
# Strip libraries / executables, we are not going to debug them.
%define strip_files %{i}/{lib,bin}
# Remove documentation, get it online.
%define drop_files %{i}/share
# Don't need archive libraries.
rm -f %{i}/lib/*.{l,}a
