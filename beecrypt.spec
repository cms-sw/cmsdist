### RPM external beecrypt 4.1.2
Requires: gcc-wrapper
Source: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%v.tar.gz

%build
## IMPORT gcc-wrapper
./configure --prefix=%i --without-python --without-java
make
