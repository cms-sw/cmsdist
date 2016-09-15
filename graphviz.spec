### RPM external graphviz 2.16.1
Source: http://www.graphviz.org/pub/%{n}/ARCHIVE/%{n}-%{realversion}.tar.gz  
Requires: expat zlib libjpg libpng 

%prep
%setup -n %{n}-%{realversion}

%build
which gcc
case %cmsplatf in
    slc*)
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
  --with-jpegincludedir=$LIBJPG_ROOT/include \
  --with-jpeglibdir=$LIBJPG_ROOT/lib \
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
  --disable-sharp \
  --disable-guile \
  --disable-java \
  --disable-lua \
  --disable-ocaml \
  --disable-perl \
  --disable-php \
  --disable-python \
  --prefix=%{i} \
  $ADDITIONAL_OPTIONS

# Probably the configure should just be remade on Darwin, but it builds
# as-is with this small cleanup
#perl -p -i -e "s|-lexpat||g;s|-ljpeg||g" configure
# make %makeprocesses
make 

%install
make install
%define drop_files %{i}/share
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig

# To match configure options above
case %cmsplatf in
    slc*)
        ln -s dot_static %i/bin/dot
    ;;
esac
# Drop static libraries.
rm -rf %i/lib/*.{l,}a
