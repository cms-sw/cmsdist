### RPM external sqlite 3.7.10
Source: http://www.sqlite.org/sqlite-autoconf-3071000.tar.gz

%prep
%setup -n sqlite-autoconf-3071000

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
