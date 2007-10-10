### RPM external cmake 2.4.2-CMS3
%define downloaddir %(echo %version | cut -d. -f1,2)
Source: http://www.cmake.org/files/v%{downloaddir}/%n-%realversion.tar.gz
#Patch1: cmake

#We are using system zlib for the online builds:
%if "%{?online_release:set}" != "set"
Requires: zlib
%endif

%prep

%setup -n cmake-%realversion
#%patch1 -p1

%build
./configure --prefix=%i
make %makeprocesses
