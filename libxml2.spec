### RPM external libxml2 2.6.23-wt1
Source: ftp://xmlsoft.org/%n/%n-%realversion.tar.gz
Requires: zlib
%prep
%setup -n %n-%realversion
%build
./configure --prefix=%i --with-zlib=$ZLIB_ROOT --without-python
make %makeprocesses
