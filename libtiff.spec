### RPM external libtiff 3.9.4
Source: http://download.osgeo.org/libtiff/tiff-%{realversion}.zip
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Requires: libjpg
%if "%online" != "true"
Requires: zlib
%endif

%prep
%setup -n tiff-%{realversion}
%build
./configure --prefix=%{i} --disable-static \
            --with-zlib-lib-dir=$ZLIB_ROOT/lib \
            --with-zlib-include-dir=$ZLIB_ROOT/include \
            --with-jpeg-lib-dir=$LIBJPG_ROOT/lib \
            --with-jpeg-include-dir=$LIBJPG_ROOT/include 
                          
make %makeprocesses

%install
make install
# Strip libraries / executables, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;
find %i/bin -type f -perm -a+x -exec strip {} \;
# Remove documentation, get it online.
rm -rf %i/share

%post
%{relocateConfig}lib/libtiff.la
%{relocateConfig}lib/libtiffxx.la
