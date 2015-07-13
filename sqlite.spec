### RPM external sqlite 3.8.10.2
Source: https://www.sqlite.org/2015/sqlite-autoconf-3081002.tar.gz

%prep
%setup -n sqlite-autoconf-3081002

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} --disable-static
make

%install
make install
%define drop_files %{i}/share/man
%define strip_files %{i}/lib
