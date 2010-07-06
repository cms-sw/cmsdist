### RPM external libtiff 3.8.2

Source: http://dl.maptools.org/dl/libtiff/tiff-%{realversion}.zip
Requires: libjpg
Requires: zlib

%prep
%setup -n tiff-%{realversion}
%build
./configure --prefix=%{i} \
            --with-zlib-lib-dir=$ZLIB_ROOT/lib \
            --with-zlib-include-dir=$ZLIB_ROOT/include \
            --with-jpeg-lib-dir=$LIBJPG_ROOT/lib \
            --with-jpeg-include-dir=$LIBJPG_ROOT/include 
                          
make %makeprocesses

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.libtiff.org/"/>
    <lib name="tiff"/>
    <client>
      <environment name="LIBTIFF_BASE" default="%i"/>
      <environment name="LIBDIR" default="$LIBTIFF_BASE/lib"/>
      <environment name="INCLUDE" default="$LIBTIFF_BASE/include"/>
    </client>
    <use name="libjpg"/>
    <use name="zlib"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}lib/libtiff.la
%{relocateConfig}lib/libtiffxx.la
%{relocateConfig}etc/scram.d/%n.xml
