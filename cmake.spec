### RPM external cmake 2.4.2
Requires: gcc-wrapper
%define downloaddir %(echo %v | cut -d. -f1,2)
Source: http://www.cmake.org/files/v%{downloaddir}/%n-%v.tar.gz
#Patch1: cmake
Requires: zlib

%prep

%setup -n cmake-%v
#%patch1 -p1

%build
## IMPORT gcc-wrapper
./configure --prefix=%i
make %makeprocesses
