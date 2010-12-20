### RPM external libxslt 1.1.15
Source: ftp://xmlsoft.org/%n/%n-%v.tar.gz

Requires: libxml2

%build
./configure --prefix=%i --with-libxml-prefix=$LIBXML2_ROOT
make %makeprocesses
