### RPM external sqlite 3.8.11.1
Source: https://www.sqlite.org/2015/sqlite-autoconf-3081101.tar.gz

%prep
%setup -n sqlite-autoconf-3081101

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
