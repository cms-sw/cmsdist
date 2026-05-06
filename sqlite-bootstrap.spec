### RPM external sqlite-bootstrap 3.53.1
%define sqlite_file sqlite-autoconf-3530100
AutoReqProv: no
Source: https://www.sqlite.org/2026/%{sqlite_file}.tar.gz

%prep
%setup -n %{sqlite_file}

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
