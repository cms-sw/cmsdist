### RPM external sqlite 3.20.1
Source: http://www.sqlite.org/2017/sqlite-autoconf-3200100.tar.gz

%prep
%setup -n sqlite-autoconf-3200100

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
