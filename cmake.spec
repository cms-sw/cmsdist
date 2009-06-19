### RPM external cmake 2.4.6
%define downloaddir %(echo %realversion | cut -d. -f1,2)
Source: http://www.cmake.org/files/v%{downloaddir}/%n-%realversion.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo flase;; esac)
#Patch1: cmake

#We are using system zlib for the online builds:
%if "%online" != "true"
Requires: zlib
%endif

%prep

%setup -n cmake-%realversion
#%patch1 -p1

%build
./configure --prefix=%i
make %makeprocesses
