### RPM external libxml2 2.6.23
Requires: gcc-wrapper
Source: ftp://xmlsoft.org/%n/%n-%v.tar.gz
Requires: zlib

%build
## IMPORT gcc-wrapper
./configure --prefix=%i --with-zlib=$ZLIB_ROOT
make %makeprocesses
