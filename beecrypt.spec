### RPM external beecrypt 3.1.0
Source: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%v.tar.gz

%build
./configure --prefix=%i --without-python --without-java
make
