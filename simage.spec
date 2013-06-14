### RPM external simage 1.6.1
Source: http://ftp.coin3d.org/coin/src/all/%{n}-%{realversion}.tar.gz
%define tmpplatf %(echo %cmsplatf | cut -d_ -f2)

Requires: libungif libjpg zlib libpng 
%if "%tmpplatf" != "amd64" 
Requires: libtiff
%endif

%prep 
%setup -n %{n}-%{realversion}

%build
CONFIGURE_ENV=
CONFIGURE_OPTS="--with-tiff=$LIBTIFF_ROOT"
%if "%tmpplatf" == "amd64"
CONFIGURE_ENV="LD=gcc"
CONFIGURE_OPTS="--without-tiff"
%endif

./configure $CONFIGURE_ENV --prefix=%i \
            $CONFIGURE_OPTS \
            --with-ungif=$LIBUNGIF_ROOT \
            --with-jpeg=$LIBJPG_ROOT \
            --with-zlib=$ZLIB_ROOT \
            --with-png=$LIBPNG_ROOT \
            --without-oggvorbis 
make 

%install
make install

%post
%{relocateConfig}bin/simage-config
%{relocateConfig}lib/libsimage.la
%{relocateConfig}share/Coin/conf/simage-default.cfg
