### RPM external libtiff 3.9.4

Source: http://download.osgeo.org/libtiff/tiff-%{realversion}.zip
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

%post
%{relocateConfig}lib/libtiff.la
%{relocateConfig}lib/libtiffxx.la
