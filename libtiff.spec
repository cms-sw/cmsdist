### RPM external libtiff 3.8.2
Source: http://dl.maptools.org/dl/libtiff/tiff-%{v}.zip
Requires: libjpg
Requires: zlib

%prep
%setup -n tiff-%{v}
%build
./configure --prefix=%{i} \
            --with-zlib-lib-dir=$ZLIB_ROOT/lib \
            --with-zlib-include-dir=$ZLIB_ROOT/include \
            --with-jpeg-lib-dir=$LIBJPG_ROOT/lib \
            --with-jpeg-include-dir=$LIBJPG_ROOT/include 
                          
make %makeprocesses
