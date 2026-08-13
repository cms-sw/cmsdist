### RPM external sqlite 3.48.0
Requires: zlib
Source: https://www.sqlite.org/2025/sqlite-autoconf-3480000.tar.gz
BuildRequires: gmake

%prep
%setup -n sqlite-autoconf-3480000

%build
CFLAGS=-I${ZLIB_ROOT}/include LDFLAGS=-L${ZLIB_ROOT}/lib \
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
