### RPM external sqlite 3.41.2
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
