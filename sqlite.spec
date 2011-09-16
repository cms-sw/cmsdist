### RPM external sqlite 3.6.23
Source: http://www.sqlite.org/sqlite-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i --disable-tcl --disable-static
make %makeprocesses

%install
make install
rm -rf %i/lib/pkgconfig
find %i/lib -type f -perm -a+x -exec strip {} \;
rm -f %i/lib/*.{l,}a
