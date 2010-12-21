### RPM external swig 2.0.1
## INITENV SET SWIG_HOME %i
## INITENV SET SWIG_LIB  %i/share/swig/%realversion

Source: http://switch.dl.sourceforge.net/sourceforge/swig/%n-%realversion.tar.gz

%build
./configure --without-pcre --prefix=%i
make %makeprocesses
