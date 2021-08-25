### RPM external sqlite 3.22.0
Source: https://www.sqlite.org/2018/sqlite-autoconf-3220000.tar.gz
Requires: zlib

%prep
%setup -n sqlite-autoconf-3220000

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking \
            CPPFLAGS="-I$ZLIB_ROOT/include" LDFLAGS="-L$ZLIB_ROOT/lib"
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
