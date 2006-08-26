### RPM external rpm 4.4.6
Source: http://wraptastic.org/pub/rpm-4.4.x/%n-%v.tar.gz
Requires: zlib 
%build
./configure --prefix=%i --with-zlib=$ZLIB_ROOT  --without-selinux --without-lua --without-python -without-libintl
make %makeprocesses
