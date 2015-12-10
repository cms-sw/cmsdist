### RPM external libtiff 3.9.4
Source: http://download.osgeo.org/libtiff/tiff-%{realversion}.zip
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Requires: libjpg
%if "%online" != "true"
Requires: zlib
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -n tiff-%{realversion}
%build
./configure --prefix=%{i} --disable-static \
            --with-zlib-lib-dir=$ZLIB_ROOT/lib \
            --with-zlib-include-dir=$ZLIB_ROOT/include \
            --with-jpeg-lib-dir=$LIBJPG_ROOT/lib \
            --with-jpeg-include-dir=$LIBJPG_ROOT/include \
            --without-x \
            CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags"
                          
make %makeprocesses

%install
make install
# Strip libraries / executables, we are not going to debug them.
%define strip_files %i/{lib,bin}
# Remove documentation, get it online.
%define drop_files %i/share
# Don't need archive libraries.
rm -f %i/lib/*.{l,}a
