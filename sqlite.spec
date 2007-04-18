### RPM external sqlite 3.3.5
Requires: gcc-wrapper
Source: http://www.sqlite.org/%{n}-%{v}.tar.gz
%build
## IMPORT gcc-wrapper
./configure --prefix=%i --disable-tcl
make %makeprocesses
