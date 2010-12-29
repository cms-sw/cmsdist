### RPM external swig 2.0.1
## INITENV SET SWIG_HOME SWIG_ROOT
Source: http://switch.dl.sourceforge.net/sourceforge/swig/%n-%realversion.tar.gz

%build
./configure --without-pcre --prefix=%i
make %makeprocesses
