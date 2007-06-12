### RPM external beecrypt 3.1.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%v.tar.gz

%build
./configure --prefix=%i --without-python --without-java
make
