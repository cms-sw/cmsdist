### RPM external graphviz 2.38.0
Source: http://www.graphviz.org/pub/%{n}/ARCHIVE/%{n}-%{realversion}.tar.gz  
Requires: expat zlib libjpeg-turbo libpng

%prep
%setup -n %{n}-%{realversion}

%build
case %cmsplatf in
    slc*|fc*)
        ADDITIONAL_OPTIONS="--with-freetype2=no --disable-shared --enable-static --disable-ltdl"
    ;;
    osx*)
        ADDITIONAL_OPTIONS="--with-freetype2=no"
    ;;
esac
./configure \
  --disable-silent-rules \
  --with-expatlibdir=$EXPAT_ROOT/lib \
  --with-expatincludedir=$EXPAT_ROOT/include \
  --with-zincludedir=$ZLIB_ROOT/include \
  --with-zlibdir=$ZLIB_ROOT/lib \
  --with-pngincludedir=$LIBPNG_ROOT/include \
  --with-pnglibdir=$LIBPNG_ROOT/lib \
  --with-jpegincludedir=$LIBJPEG_TURBO_ROOT/include \
  --with-jpeglibdir=$LIBJPEG_TURBO_ROOT/lib \
  --without-x \
  --without-tclsh \
  --without-tcl \
  --without-fontconfig \
  --without-tk \
  --without-perl \
  --without-python \
  --without-ruby \
  --disable-ruby \
  --disable-perl \
  --without-pangocairo \
  --without-fontconfig \
  --without-gdk-pixbuf \
  --with-libgd=no \
  --disable-sharp \
  --disable-guile \
  --disable-java \
  --disable-lua \
  --disable-ocaml \
  --disable-perl \
  --disable-php \
  --disable-python \
  --with-qt=no \
  --prefix=%{i} \
  $ADDITIONAL_OPTIONS

make %{makeprocesses}

%install
make install
%define drop_files %{i}/share

rm -rf %{i}/lib/pkgconfig

# To match configure options above
case %{cmsplatf} in
    slc*|fc*)
        ln -s dot_static %{i}/bin/dot
    ;;
esac
# Drop static libraries.
rm -rf %{i}/lib/*.{l,}a
