### RPM external sqlite-bootstrap 3.48.0
AutoReqProv: no
Source: https://www.sqlite.org/2025/sqlite-autoconf-3480000.tar.gz

%prep
%setup -n sqlite-autoconf-3480000

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
