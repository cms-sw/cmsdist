### RPM external swig 1.3.29
Requires: gcc-wrapper
## INITENV SET SWIG_HOME SWIG_ROOT
Source: http://switch.dl.sourceforge.net/sourceforge/swig/%n-%v.tar.gz

%build
## IMPORT gcc-wrapper
./configure --prefix=%i
make %makeprocesses
