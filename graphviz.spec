### RPM external graphviz 2.16.1
Source: http://www.graphviz.org/pub/%{n}/ARCHIVE/%{n}-%{realversion}.tar.gz  
Requires: expat zlib libjpg libpng 

%prep
%setup -n %{n}-%{realversion}

%build
which gcc
LIB64_SUFFIX=
case %cmsplatf in
    slc*_ia32_* )
        export LD_LIBRARY_PATH=`echo $LD_LIBRARY_PATH | sed -e 's|lib64|lib|g'`
        ADDITIONAL_OPTIONS="--with-freetype2=no --disable-shared --enable-static --disable-libtdl"
    ;;
    slc*_amd64_* )
        LIB64_SUFFIX=64
        ADDITIONAL_OPTIONS="--with-freetype2=no --disable-shared --enable-static --disable-ltdl"
    ;;
    osx* )
        ADDITIONAL_OPTIONS="--with-freetype2=no"
    ;;
esac
./configure \
  --with-expatlibdir=$EXPAT_ROOT/lib$LIB64_SUFFIX \
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

# This is a workaround for the fact that sort from coreutils 5.96 doesn't 
# like "sort +0 -1", not really something specific to ppc64/ydl5.0
if [ "$(uname -m)" == "ppc64" ]
then
perl -p -i -e "s|\+0 \-1|-k1,1|g" dotneato/common/Makefile
fi
# Probably the configure should just be remade on Darwin, but it builds
# as-is with this small cleanup
perl -p -i -e "s|-lexpat||g;s|-ljpeg||g" configure
# make %makeprocesses
make 

%install
make install
# To match configure options above
case %cmsplatf in
    slc*_ia32_* | slc*_amd64_*)
        ln -s dot_static %i/bin/dot
    ;;
esac

%post
%{relocateCmsFiles} `find $RPM_INSTALL_PREFIX/%pkgrel/lib -name *.la`
