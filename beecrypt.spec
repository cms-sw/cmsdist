### RPM external beecrypt 4.1.2
Source: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%v.tar.gz

%build
./configure --prefix=%i --without-python --without-java
make
