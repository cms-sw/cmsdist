### RPM external libtiff 4.6.0
Source: https://github.com/libsdl-org/libtiff/archive/refs/tags/v%{realversion}.tar.gz
Requires: libjpeg-turbo zlib xz zstd
BuildRequires: autotools gmake

%prep
%setup -n libtiff-%{realversion}

%build
autoreconf -fiv
./configure --prefix=%{i} --disable-static \
            --with-zstd-lib-dir=${ZSTD_ROOT}/lib \
            --with-zstd-include-dir=${ZSTD_ROOT}/include \
            --with-lzma-lib-dir=${XZ_ROOT}/lib \
            --with-lzma-include-dir=${XZ_ROOT}/include \
            --with-zlib-lib-dir=${ZLIB_ROOT}/lib \
            --with-zlib-include-dir=${ZLIB_ROOT}/include \
            --with-jpeg-lib-dir=${LIBJPEG_TURBO_ROOT}/lib64 \
            --with-jpeg-include-dir=${LIBJPEG_TURBO_ROOT}/include \
            --disable-dependency-tracking \
            --without-x

make %{makeprocesses}

%install
make install
# Strip libraries / executables, we are not going to debug them.
%define strip_files %{i}/{lib,bin}
# Remove documentation, get it online.
%define drop_files %{i}/share
# Don't need archive libraries.
rm -f %{i}/lib/*.{l,}a
