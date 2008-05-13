### RPM external cmake 2.4.6-CMS20
%define downloaddir %(echo %realversion | cut -d. -f1,2)
Source: http://www.cmake.org/files/v%{downloaddir}/%n-%realversion.tar.gz
#Patch1: cmake

#We are using system zlib for the online builds:
%if "%cmsplatf" != "slc4onl_ia32_gcc346"
Requires: zlib
%endif

%prep

%setup -n cmake-%realversion
#%patch1 -p1

%build
./configure --prefix=%i
make %makeprocesses
