### RPM external swig 1.3.28
## INITENV SET SWIG_HOME SWIG_ROOT
Source: http://easynews.dl.sourceforge.net/sourceforge/%n/%n-%v.tar.gz

%build
./configure --prefix=%i
make %makeprocesses
