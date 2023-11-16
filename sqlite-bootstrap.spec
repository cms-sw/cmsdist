### RPM external sqlite-bootstrap 3.36.0
AutoReqProv: no
Source: https://www.sqlite.org/2021/sqlite-autoconf-3360000.tar.gz

%prep
%setup -n sqlite-autoconf-3360000

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
