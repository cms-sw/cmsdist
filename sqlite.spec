### RPM external sqlite 3.12.2
Source: https://www.sqlite.org/2016/sqlite-autoconf-3120200.tar.gz

%prep
%setup -n sqlite-autoconf-3120200

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
