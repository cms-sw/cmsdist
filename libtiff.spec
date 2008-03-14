### RPM external libtiff 3.8.2-CMS18

Source: http://dl.maptools.org/dl/libtiff/tiff-%{realversion}.zip

%if "%{?online_release:set}" != "set"
Requires: zlib
%endif

%if "%{?online_release:set}" == "set"
Requires: onlinesystemtools
%endif

Requires: libjpg

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
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.libtiff.org/"></info>
<lib name=tiff>
<Client>
 <Environment name=LIBTIFF_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LIBTIFF_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$LIBTIFF_BASE/include"></Environment>
</Client>
<use name=libjpg>
<use name=zlib>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}lib/libtiff.la
%{relocateConfig}lib/libtiffxx.la
%{relocateConfig}etc/scram.d/%n
