### RPM external rpm 4.4.9-wt1
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
Source: http://rpm5.org/files/rpm/rpm-4.4/%n-%realversion.tar.gz
Requires: beecrypt bz2lib neon expat db4 expat elfutils zlib
Patch0: rpm-4.4.9-enum
Patch1: rpm-4.4.9-rpmps
%if "%(echo %{cmsos} | cut -d_ -f 2 | sed -e 's|.*64.*|64|')" == "64"
%define libdir lib64 
%else
%define libdir lib
%endif
%prep 
%setup -n %n-%{realversion}
%patch0 -p0
%patch1 -p0
%build
#export LIBS="-lexpat"
export CFLAGS="-fPIC"
export CPPFLAGS="-I$BEECRYPT_ROOT/include/beecrypt -I$BZ2LIB_ROOT/include -I$NEON_ROOT/include/neon -I$DB4_ROOT/include -I$EXPAT_ROOT/include/expat -I$ELFUTILS_ROOT/include -I$ZLIB_ROOT/include"
export LDFLAGS="-L$BEECRYPT_ROOT/%libdir -L$BZ2LIB_ROOT/lib -L$NEON_ROOT/lib -L$DB4_ROOT/lib -L$EXPAT_ROOT/%libdir -L$ELFUTILS_ROOT/lib -L$ZLIB_ROOT/lib -lexpat"
#FIXME: this does not seem to work and we still get /usr/bin/python in some of the files.
export __PYTHON="/usr/bin/env python"
perl -p -i -e "s|\@WITH_NEON_LIB\@|$NEON_ROOT/lib/libneon.a|;
" `find . -name \*.in` 
perl -p -i -e "s|#undef HAVE_NEON_NE_GET_RESPONSE_HEADER|#define HAVE_NEON_NE_GET_RESPONSE_HEADER 1|" config.h.in

./configure --prefix=%i --disable-nls --without-selinux --with-lua=no --without-python --without-libintl --without-perl
(cd zlib; make)
make %makeprocesses
perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|" scripts/get_magic.pl \
                                                      scripts/rpmdiff.cgi \
                                                      scripts/cpanflute2 \
                                                      scripts/perldeps.pl \
                                                      db/dist/camelize.pl 


%install
make install
perl -p -i -e "s|#\!/usr/bin/python(.*)|#!/usr/bin/env python$1|" %i/lib/rpm/symclash.py

mkdir -p %{i}/etc/profile.d
(echo "#!/bin/sh"; \
 echo "source $BEECRYPT_ROOT/etc/profile.d/init.sh"; \
 echo "source $NEON_ROOT/etc/profile.d/init.sh"; \
 echo "source $EXPAT_ROOT/etc/profile.d/init.sh"; \
 echo "source $ELFUTILS_ROOT/etc/profile.d/init.sh"; \
 echo "source $BZ2LIB_ROOT/etc/profile.d/init.sh"; \
 echo "source $ZLIB_ROOT/etc/profile.d/init.sh"; \
 echo "source $DB4_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $BEECRYPT_ROOT/etc/profile.d/init.csh"; \
 echo "source $NEON_ROOT/etc/profile.d/init.csh"; \
 echo "source $EXPAT_ROOT/etc/profile.d/init.csh"; \
 echo "source $ELFUTILS_ROOT/etc/profile.d/init.csh"; \
 echo "source $BZ2LIB_ROOT/etc/profile.d/init.csh"; \
 echo "source $ZLIB_ROOT/etc/profile.d/init.csh"; \
 echo "source $DB4_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|" `grep -r %instroot $RPM_INSTALL_PREFIX/%pkgrel | grep -v Binary | cut -d: -f1`
