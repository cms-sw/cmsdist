### RPM external rpm 4.3.3-18_nonptl
Source: http://elmer.web.cern.ch/elmer/rpm-4.3.3-18_nonptl.tar.gz
Requires: zlib beecrypt bz2lib 
%build
export CFLAGS="-I$BEECRYPT_ROOT/include/beecrypt -I$BEECRYPT_ROOT/include -I$BZ2LIB_ROOT/include"
export LDFLAGS="-L$BEECRYPT_ROOT/lib -L$BZ2LIB_ROOT/lib"
./configure --prefix=%i --with-zlib=$ZLIB_ROOT  --without-selinux --without-lua --without-python -without-libintl
make %makeprocesses
perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|" scripts/get_magic.pl \
                                                      scripts/rpmdiff.cgi \
                                                      scripts/cpanflute2 \
                                                      scripts/perldeps.pl \
                                                      db/dist/camelize.pl 
%install
make install
(cd %i; tar czvf %_sourcedir/rpm-bootstrap-%v.tar.gz .)
%post
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|" `grep -r %instroot $RPM_INSTALL_PREFIX/%pkgrel | grep -v Binary | cut -d: -f1`
