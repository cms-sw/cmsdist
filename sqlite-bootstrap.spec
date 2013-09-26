### RPM external sqlite-bootstrap 3.7.17
Source: http://www.sqlite.org/2013/sqlite-autoconf-3071700.tar.gz

%prep
%setup -n sqlite-autoconf-3071700

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
