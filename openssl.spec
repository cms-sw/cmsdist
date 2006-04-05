### RPM external openssl 0.9.7d
Source: http://www.openssl.org/source/%n-%v.tar.gz

%build
./config --prefix=%i shared
make
