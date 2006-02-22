### RPM external sqlite 3.2.1
Source: http://www.sqlite.org/%{n}-%{v}.tar.gz
%build
./configure --prefix=%i --disable-tcl
make
