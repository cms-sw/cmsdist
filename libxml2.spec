### RPM external libxml2 2.6.23
Source: ftp://xmlsoft.org/%n/%n-%v.tar.gz
Requires: zlib

%build
./configure --prefix=%i --with-zlib=$ZLIB_ROOT
make %makeprocesses
