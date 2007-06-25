### RPM external rpm 4.4.6-wt1
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV SET LIBRPMALIAS_FILENAME %{i}/lib/rpm/rpmpopt-%{realversion}
## INITENV SET LIBRPMRC_FILENAME %{i}/lib/rpm/rpmrc
## INITENV SET RPM_MACROFILES %{i}/lib/rpm/macros
## INITENV SET USRLIBRPM %{i}/lib/rpm
## INITENV SET RPMCONFIGDIR %{i}/lib/rpm
## INITENV SET SYSCONFIGDIR %{i}/lib/rpm
Source: http://rpm5.org/files/rpm/rpm-4.4/%n-%realversion.tar.gz
Requires: beecrypt bz2lib neon expat db4 expat elfutils zlib
Patch0: rpm-4.4.9-enum
Patch1: rpm-4.4.9-rpmps
Patch2: rpm-4.4.9-popt
Patch3: rpm-4.4.9-macrofiles
Patch4: rpm-4.4.6
%if "%(echo %{cmsos} | cut -d_ -f 2 | sed -e 's|.*64.*|64|')" == "64"
%define libdir lib64 
%else
%define libdir lib
%endif
%prep 
%setup -n %n-%{realversion}
%if "%{realversion}" == "4.4.9"
%patch0 -p0
%endif

%patch1 -p0

%if "%{realversion}" == "4.4.9"
%patch2 -p0
%patch3 -p0
%endif

%if "%{realversion}" == "4.4.6"
%patch4 -p0
%endif
rm -rf neon sqlite beecrypt elfutils zlib 
%build
#export LIBS="-lexpat"
export CFLAGS="-fPIC"
export CPPFLAGS="-I$BEECRYPT_ROOT/include -I$BEECRYPT_ROOT/include/beecrypt -I$BZ2LIB_ROOT/include -I$NEON_ROOT/include/neon -I$DB4_ROOT/include -I$EXPAT_ROOT/include/expat -I$ELFUTILS_ROOT/include -I$ZLIB_ROOT/include"
export LDFLAGS="-L$BEECRYPT_ROOT/%libdir -L$BZ2LIB_ROOT/lib -L$NEON_ROOT/lib -L$DB4_ROOT/lib -L$EXPAT_ROOT/%libdir -L$ELFUTILS_ROOT/lib -L$ZLIB_ROOT/lib -lz -lexpat -lbeecrypt -lbz2 -lneon"
#FIXME: this does not seem to work and we still get /usr/bin/python in some of the files.
export __PYTHON="/usr/bin/env python"
perl -p -i -e "s|\@WITH_NEON_LIB\@|$NEON_ROOT/lib/libneon.a|;
" `find . -name \*.in` 
perl -p -i -e "s|#undef HAVE_NEON_NE_GET_RESPONSE_HEADER|#define HAVE_NEON_NE_GET_RESPONSE_HEADER 1|;
               s|#undef HAVE_BZ2_1_0|#define HAVE_BZ2_1_0|;
               s|#undef HAVE_GETPASSPHRASE||;
               s|#undef HAVE_LUA||" config.h.in

varprefix=%{instroot}/%{cmsplatf}/var ./configure --prefix=%i --disable-nls --without-selinux --without-python --without-libintl --without-perl 
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
# The following patches the rpmrc to make sure that rpm macros are only picked up from
# what we distribute and not /etc or ~/
perl -p -i -e "s!:/etc/[^:]*!!g;
               s!~/[^:]*!!g" %i/lib/rpm/rpmrc

# This is for compatibility with rpm 4.3.3
perl -p -i -e "s!^.buildroot!#%%buildroot!;
               s!^%%_repackage_dir.*/var/spool/repackage!%%_repackage_dir     %{instroot}/%{cmsplatf}/var/spool/repackage!" %i/lib/rpm/macros
mkdir -p %{instroot}/%{cmsplatf}/var/spool/repackage
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
%files
%{i}
%{instroot}/%{cmsplatf}/var/spool/repackage

