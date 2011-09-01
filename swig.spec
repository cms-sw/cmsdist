### RPM external swig 2.0.4
## INITENV SET SWIG_HOME %i
## INITENV SET SWIG_LIB  %i/share/swig/%realversion

Source: http://switch.dl.sourceforge.net/sourceforge/swig/%n-%realversion.tar.gz

%build
./configure --without-pcre --prefix=%i \
            CC="`which gcc`" CXX="`which c++`" LD="`which c++`"
make %makeprocesses
