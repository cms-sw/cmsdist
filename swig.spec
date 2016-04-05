### RPM external swig 2.0.12
## INITENV SET SWIG_HOME %i
## INITENV SET SWIG_LIB  %i/share/swig/%realversion

Source: http://downloads.sourceforge.net/sourceforge/swig/swig/%n-%realversion.tar.gz

%prep
%setup -n %n-%realversion

%build
./configure --without-pcre --prefix=%i \
            CC="$(which gcc)" CXX="$(which g++)" LD="$(which g++)"
make %makeprocesses CXXFLAGS="-Wall -W -ansi -pedantic"

%define strip_files %i/bin/{swig,ccache-swig}
