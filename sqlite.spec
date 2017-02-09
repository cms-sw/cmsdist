### RPM external sqlite 3.16.2
Source: http://sqlite.org/2016/sqlite-autoconf-3150100.tar.gz

%prep
%setup -n sqlite-autoconf-3150100

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
