### RPM external sqlite 3.21.0
Source: https://www.sqlite.org/2017/sqlite-autoconf-3210000.tar.gz

%prep
%setup -n sqlite-autoconf-3210000

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
