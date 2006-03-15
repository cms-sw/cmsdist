### RPM external cmake 1.8.3
%define download dir %(echo %v | cut -d. -f1,2)
Source: http://www.cmake.org/files/v1.8/%n-%v.tar.gz
%build
./configure --prefix=%i
make %makeprocesses
