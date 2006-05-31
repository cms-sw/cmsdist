### RPM external cmake 1.8.3
%define download dir %(echo %v | cut -d. -f1,2)
Source: http://www.cmake.org/files/v1.8/%n-%v.tar.gz
Patch1: cmake

%prep

%setup -n cmake-%v
%patch1 -p1

%build
./configure --prefix=%i
make %makeprocesses
