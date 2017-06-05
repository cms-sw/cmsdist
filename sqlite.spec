### RPM external sqlite 3.19.2
Source: http://www.sqlite.org/2017/sqlite-autoconf-3190200.tar.gz

%prep
%setup -n sqlite-autoconf-3190200

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
