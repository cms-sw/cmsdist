### RPM external cmake 2.8.1
%define downloaddir %(echo %realversion | cut -d. -f1,2)
Source: http://www.cmake.org/files/v%{downloaddir}/%n-%realversion.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)
#Patch1: cmake
Patch2: cmake-osx-nld

#We are using system zlib for the online builds:
%if "%online" != "true"
Requires: zlib
%endif

%prep

%setup -n cmake-%realversion
#%patch1 -p1
%if "%(echo %{cmsos} | cut -d_ -f 1 | sed -e 's|osx.*|osx|')" == "osx"
%patch2 -p0
%endif

%build
./configure --prefix=%i
make %makeprocesses
