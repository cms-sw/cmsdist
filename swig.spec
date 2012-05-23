### RPM external swig 2.0.4
## INITENV SET SWIG_HOME %i
## INITENV SET SWIG_LIB  %i/share/swig/%realversion

Source: http://downloads.sourceforge.net/sourceforge/swig/swig/%n-%realversion.tar.gz

Patch0: swig-2.0.4-fix-gcc47-cxx11

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -n %n-%realversion

# Apply C++11 / gcc 4.7.x fixes only if using a 47x architecture.
# See http://gcc.gnu.org/gcc-4.7/porting_to.html
case %cmsplatf in
  *gcc4[789]*)
%patch0 -p1
  ;;
esac

%build
./configure --without-pcre --prefix=%i \
            CC="`which gcc`" CXX="`which %cms_cxx`" LD="`which %cms_cxx`" 
make %makeprocesses CXXFLAGS="-Wall -W -ansi -pedantic %cms_cxxflags"

%define strip_files %i/bin/{swig,ccache-swig}
