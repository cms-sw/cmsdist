### RPM external rpm 4.4.6
Source: http://wraptastic.org/pub/rpm-4.4.x/%n-%v.tar.gz

%build
./configure --prefix=%i --without-lua --without-python -without-libintl
make %makeprocesses
