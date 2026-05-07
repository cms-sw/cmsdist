### RPM external sqlite 3.53.1
%define sqlite_file sqlite-autoconf-3530100
Requires: zlib
Source: https://www.sqlite.org/2026/%{sqlite_file}.tar.gz
BuildRequires: gmake

%prep
%setup -n %{sqlite_file}

%build
CFLAGS=-I${ZLIB_ROOT}/include LDFLAGS=-L${ZLIB_ROOT}/lib \
./configure --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
