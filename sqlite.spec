### RPM external sqlite 3.8.1
Source: http://www.sqlite.org/2013/sqlite-autoconf-3080100.tar.gz

%prep
%setup -n sqlite-autoconf-3080100

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
make %{makeprocesses}

%install
make install
%define drop_files %{i}/share/man
%define strip_files %{i}/lib
