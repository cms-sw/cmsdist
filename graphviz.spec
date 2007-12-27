### RPM external graphviz 1.9-CMS19
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%{n}-%{realversion}.tar.gz  
Requires: expat zlib libjpg libpng 
Patch0: graphviz

%prep
%setup -n %{n}-%{realversion}
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

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.research.att.com/sw/tools/graphviz/"></info>
<Client>
 <Environment name=GRAPHVIZ_BASE default="%i"></Environment>
 <Environment name=GRAPHVIZ_BINDIR default="$GRAPHVIZ_BASE/bin"></Environment>
 <Environment name=LIBDIR default="$GRAPHVIZ_BASE/lib/graphviz"></Environment>
</Client>
<Runtime name=PATH value="$GRAPHVIZ_BINDIR" type=path>
<Use name=expat>
<Use name=zlib>
<Use name=libjpg>
<use name=libpng>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}bin/dotneato-config `find $RPM_INSTALL_PREFIX/%pkgrel/lib/graphviz -name *.la`
%{relocateConfig}etc/scram.d/%n
