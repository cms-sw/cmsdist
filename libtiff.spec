### RPM external libtiff 4.0.10
Source: http://download.osgeo.org/libtiff/tiff-%{realversion}.zip

Requires: libjpeg-turbo zlib

%prep
%setup -n tiff-%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
%get_config_sub ./config/config.sub
%get_config_guess ./config/config.guess
chmod +x ./config/config.{sub,guess}

%build
./configure --prefix=%{i} --disable-static \
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
