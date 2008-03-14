### RPM external sqlite 3.3.5
Source: http://www.sqlite.org/%{n}-%{v}.tar.gz
%build
./configure --prefix=%i --disable-tcl
make %makeprocesses
