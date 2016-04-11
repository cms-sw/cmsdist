### RPM external sqlite 3.12.1
Source: https://www.sqlite.org/2016/sqlite-autoconf-3120100.tar.gz

%prep
%setup -n sqlite-autoconf-3120100

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
