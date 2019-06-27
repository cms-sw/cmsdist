### RPM external sqlite 3.22.0
Source: https://www.sqlite.org/2018/sqlite-autoconf-3220000.tar.gz

%prep
%setup -n sqlite-autoconf-3220000

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
# bla bla
