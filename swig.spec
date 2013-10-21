### RPM external swig 2.0.10
## INITENV SET SWIG_HOME %i
## INITENV SET SWIG_LIB  %i/share/swig/%realversion

%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://downloads.sourceforge.net/sourceforge/swig/swig/%n-%realversion.tar.gz

Patch0: swig-2.0.10-fix-gcc47-cxx11

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -n %n-%realversion

%patch0 -p1

%build
./configure --without-pcre --prefix=%i \
%if "%mic" == "true"
            --host=x86_64-k1om-linux  CC="icc -mmic" CXX="icpc -mmic" LD="icpc -mmic" 
%else
            CC="`which gcc`" CXX="`which %cms_cxx`" LD="`which %cms_cxx`" 
%endif
make %makeprocesses CXXFLAGS="-Wall -W -ansi -pedantic %cms_cxxflags"

%define strip_files %i/bin/{swig,ccache-swig}
