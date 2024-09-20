### RPM external sqlite 3.46.1
Source: https://www.sqlite.org/2024/sqlite-autoconf-3460100.tar.gz
Requires: zlib
BuildRequires: gmake

%prep
%setup -n sqlite-autoconf-3460100

%build
CFLAGS=-I${ZLIB_ROOT}/include LDFLAGS=-L${ZLIB_ROOT}/lib \
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
