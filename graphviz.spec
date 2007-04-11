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
  --without-tclsh \
  --without-tcl \
  --without-tk \
  --prefix=%{i}
# This is a workaround for the fact that sort from coreutils 5.96 doesn't 
# like "sort +0 -1", not really something specific to ppc64/ydl5.0
if [ "$(uname -m)" == "ppc64" ]
then
perl -p -i -e "s|\+0 \-1|-k1,1|g" dotneato/common/Makefile
fi
make
%post
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|" $RPM_INSTALL_PREFIX/%pkgrel/bin/dotneato-config `find $RPM_INSTALL_PREFIX/%pkgrel/lib/graphviz -name *.la`
