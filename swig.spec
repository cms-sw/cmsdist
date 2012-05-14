### RPM external swig 2.0.4
## INITENV SET SWIG_HOME %i
## INITENV SET SWIG_LIB  %i/share/swig/%realversion

Source: http://downloads.sourceforge.net/sourceforge/swig/swig/%n-%realversion.tar.gz

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%build
./configure --without-pcre --prefix=%i \
            CC="`which gcc`" CXX="`which %cms_cxx`" LD="`which %cms_cxx`" CXXFLAGS="%cms_cxxflags"
make %makeprocesses

%define strip_files %i/bin/{swig,ccache-swig}
