### RPM external swig 1.3.29
## INITENV SET SWIG_HOME SWIG_ROOT
Source: http://switch.dl.sourceforge.net/sourceforge/swig/%n-%v.tar.gz

%build
./configure --prefix=%i
make %makeprocesses
