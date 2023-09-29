### RPM external sqlite 3.43.1
Source: https://sqlite.org/2023/sqlite-autoconf-3430100.tar.gz
Requires: zlib

%prep
%setup -n sqlite-autoconf-3430100

%build
CFLAGS=-I${ZLIB_ROOT}/include LDFLAGS=-L${ZLIB_ROOT}/lib \
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
