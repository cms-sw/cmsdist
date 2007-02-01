### RPM external rpm 4.3.3-18_nonptl
Source: http://elmer.web.cern.ch/elmer/rpm-4.3.3-18_nonptl.tar.gz
Requires: zlib 
%build
./configure --prefix=%i --with-zlib=$ZLIB_ROOT  --without-selinux --without-lua --without-python -without-libintl
make %makeprocesses
