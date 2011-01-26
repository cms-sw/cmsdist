### RPM external sqlite 3.6.23
Source: http://www.sqlite.org/sqlite-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i --disable-tcl
make %makeprocesses

%install
make install
rm -rf %i/lib/pkgconfig
