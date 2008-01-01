### RPM external rpm 4.4.2.2-CMS19
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV SET LIBRPMALIAS_FILENAME %{i}/lib/rpm/rpmpopt-%{realversion}
## INITENV SET LIBRPMRC_FILENAME %{i}/lib/rpm/rpmrc
## INITENV SET RPM_MACROFILES %{i}/lib/rpm/macros
## INITENV SET USRLIBRPM %{i}/lib/rpm
## INITENV SET RPMMAGIC %{i}/lib/rpm/magic
## INITENV SET RPMCONFIGDIR %{i}/lib/rpm
## INITENV SET SYSCONFIGDIR %{i}/lib/rpm
Source: http://rpm.org/releases/rpm-4.4.x/rpm-%{realversion}.tar.gz
#Source: http://rpm5.org/files/rpm/rpm-4.4/%n-%realversion.tar.gz

Requires: beecrypt bz2lib neon db4 expat elfutils zlib

Patch0: rpm-4.4.9-enum
Patch1: rpm-4.4.9-rpmps
Patch2: rpm-4.4.9-popt
Patch3: rpm-4.4.9-macrofiles
Patch4: rpm-4.4.6
Patch5: rpm-4.4.2.1
Patch6: rpm-macosx
Patch7: rpm-4.4.2.2
Patch8: rpm-4.4.2.2-leopard
Patch9: rpm-4.4.x-flcompress

# Defaults here
%define libdir lib
%define soname so

%if "%(echo %{cmsos} | cut -d_ -f 2 | sed -e 's|.*64.*|64|')" == "64"
%define libdir lib64 
%endif

# On macosx SONAME is dylib
%if "%(echo %{cmsos} | cut -d_ -f 1 | sed -e 's|osx.*|osx|')" == "osx"
%define soname dylib
Provides: Kerberos
%endif

%prep 
%setup -n %n-%{realversion}
%if "%{realversion}" == "4.4.9"
%patch0 -p0
%endif

#%patch1 -p0

%if "%{realversion}" == "4.4.9"
%patch2 -p0
%patch3 -p0
%endif

%if "%{realversion}" == "4.4.6"
%patch4 -p0
%endif

%if "%{realversion}" == "4.4.2.1"
%patch5 -p0
%endif

%patch6 -p1

%if "%{realversion}" == "4.4.2.2"
%patch7 -p1
%endif

echo %(echo %{cmsos} | cut -f1 -d_)
%if "%(echo %{cmsos} | cut -f1 -d_)" == "osx105"
%patch8 -p1
%endif

%patch9 -p1

rm -rf neon sqlite beecrypt elfutils zlib 

%build
export CFLAGS="-fPIC -g -O0"
export CPPFLAGS="-I$BEECRYPT_ROOT/include -I$BEECRYPT_ROOT/include/beecrypt -I$BZ2LIB_ROOT/include -I$NEON_ROOT/include/neon -I$DB4_ROOT/include -I$EXPAT_ROOT/include/expat -I$ELFUTILS_ROOT/include -I$ZLIB_ROOT/include"
export LDFLAGS="-L$BEECRYPT_ROOT/%libdir -L$BZ2LIB_ROOT/lib -L$NEON_ROOT/lib -L$DB4_ROOT/lib -L$EXPAT_ROOT/%libdir -L$ELFUTILS_ROOT/lib -L$ZLIB_ROOT/lib -lz -lexpat -lbeecrypt -lbz2 -lneon -lpthread"
#FIXME: this does not seem to work and we still get /usr/bin/python in some of the files.
export __PYTHON="/usr/bin/env python"
perl -p -i -e "s|\@WITH_NEON_LIB\@|$NEON_ROOT/lib/libneon.a|;
s|^.*WITH_SELINUX.*$||;
s|-lselinux||;
" `find . -name \*.in` 
perl -p -i -e "s|#undef HAVE_NEON_NE_GET_RESPONSE_HEADER|#define HAVE_NEON_NE_GET_RESPONSE_HEADER 1|;
               s|#undef HAVE_BZ2_1_0|#define HAVE_BZ2_1_0|;
               s|#undef HAVE_GETPASSPHRASE||;
               s|#undef HAVE_LUA||;" config.h.in
#perl -p -i -e 's%^(WITH_DB_SUBDIR|WITH_INTERNAL_DB|DBLIBSRCS)%#$1%' configure
case `uname` in
    Darwin*)
        perl -p -i -e s'![\t]\@WITH_ZLIB_LIB\@!!' Makefile.in
        ;;
esac

varprefix=%{instroot}/%{cmsplatf}/var ./configure --prefix=%i --disable-nls --without-selinux --without-python --without-libintl  --without-perl --with-zlib-includes=$ZLIB_ROOT/include --with-zlib-lib=$ZLIB_ROOT/lib/libz.%soname --without-lua
perl -p -i -e "s|lua||" Makefile

#this does nothing...(cd zlib; make)
if ! make %makeprocesses
then
    # Very ugly hack to get rid of any kind of automatically generated dependecy on /usr/lib/beecrypt.
    toBePatched=`grep -R -e '/usr/lib[6]*[4]*/[^ ]*.la' . | grep  "\.la" | cut -f1 -d:`
    if [ "X$toBePatched" != X ]
    then
        perl -p -i -e 's|/usr/lib[6]*[4]*/[^ ]*.la||' $toBePatched 
        make %makeprocesses 
    fi
fi
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

# Removes any reference to /usr/lib/rpm in lib/rpm
perl -p -i -e 's|/usr/lib/rpm([^a-zA-Z])|%{i}/lib/rpm$1|g' \
    %{i}/lib/rpm/check-rpaths \
    %{i}/lib/rpm/check-rpaths-worker \
    %{i}/lib/rpm/cpanflute \
    %{i}/lib/rpm/cpanflute2 \
    %{i}/lib/rpm/cross-build \
    %{i}/lib/rpm/find-debuginfo.sh \
    %{i}/lib/rpm/find-provides.perl \
    %{i}/lib/rpm/find-requires.perl \
    %{i}/lib/rpm/freshen.sh \
    %{i}/lib/rpm/perldeps.pl \
    %{i}/lib/rpm/rpmdb_loadcvt \
    %{i}/lib/rpm/rpmrc \
    %{i}/lib/rpm/trpm \
    %{i}/lib/rpm/vpkg-provides.sh \
    %{i}/lib/rpm/vpkg-provides2.sh

# Changes the shebang from /usr/bin/perl to /usr/bin/env perl
perl -p -i -e 's|^#[!]/usr/bin/perl(.*)|#!/usr/bin/env perl$1|' \
    %{i}/lib/rpm/perl.prov \
    %{i}/lib/rpm/perl.req \
    %{i}/lib/rpm/rpmdiff \
    %{i}/lib/rpm/sql.prov \
    %{i}/lib/rpm/sql.req \
    %{i}/lib/rpm/tcl.req \
    %{i}/lib/rpm/magic.prov \
    %{i}/lib/rpm/magic.req \
    %{i}/lib/rpm/cpanflute

mkdir -p %{instroot}/%{cmsplatf}/var/spool/repackage

# Generates the dependencies-setup.sh/dependencies-setup.csh
# which is automatically sourced by init.sh/init.csh, providing 
# the environment for all the dependencies.
mkdir -p %{i}/etc/profile.d

echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done

perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh

ln -sf rpm/rpmpopt-%{realversion} %i/lib/rpmpopt

# Remove some of the path macros defined in macros since they could come
# from different places (e.g. from system or from macports) and this would
# lead to problems if a developer with macports builds a bootstrap package set.
for shellUtil in tar cat chgrp chmod chown cp file gpg id make mkdir mv pgp rm rsh sed ssh gzip cpio perl unzip patch grep 
do
    perl -p -i -e "s|^%__$shellUtil\s(.*)|%__$shellUtil       $shellUtil|" %i/lib/rpm/macros
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}lib/rpm/check-rpaths 
%{relocateConfig}lib/rpm/check-rpaths-worker 
%{relocateConfig}lib/rpm/cpanflute 
%{relocateConfig}lib/rpm/cpanflute2 
%{relocateConfig}lib/rpm/cross-build 
%{relocateConfig}lib/rpm/find-debuginfo.sh 
%{relocateConfig}lib/rpm/find-provides.perl 
%{relocateConfig}lib/rpm/find-requires.perl 
%{relocateConfig}lib/rpm/freshen.sh 
%{relocateConfig}lib/rpm/perldeps.pl 
%{relocateConfig}lib/rpm/rpmdb_loadcvt 
%{relocateConfig}lib/rpm/rpmrc 
%{relocateConfig}lib/rpm/trpm 
%{relocateConfig}lib/rpm/vpkg-provides.sh 
%{relocateConfig}lib/rpm/vpkg-provides2.sh
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g" `grep -r %instroot $RPM_INSTALL_PREFIX/%pkgrel | grep -v Binary | cut -d: -f1 | sort | uniq`
%files
%{i}
%{instroot}/%{cmsplatf}/var/spool/repackage
