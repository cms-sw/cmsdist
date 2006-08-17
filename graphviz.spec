### RPM external graphviz 1.9 
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%{n}-%{v}.tar.gz  
Requires: expat zlib libjpg libpng 
Patch0: graphviz

%prep
%setup -n %{n}-%{v}
%patch0 -p1

%build
./configure \
  --with-expatlibdir=$EXPAT_ROOT/lib \
  --with-expatincludedir=$EXPAT_ROOT/include \
  --with-zincludedir=$ZLIB_ROOT/include \
  --with-zlibdir=$ZLIB_ROOT/lib \
  --with-pngincludedir=$LIBJPG_ROOT/include \
  --with-pnglibdir=$LIBJPG_ROOT/lib \
  --with-jpegincludedir=$LIBPNG_ROOT/include \
  --with-jpeglibdir=$LIBPNG_ROOT/lib \
  --without-x \
  --without-tcl \
  --without-tk \
  --prefix=%{i}

make
