### RPM external rpm 4.8.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV SET RPM_CONFIGDIR %{i}/lib/rpm

# Warning! While rpm itself seems to work, at the time of writing it
# does not seem to be possible to build apt-rpm with 
Source: http://rpm.org/releases/rpm-%(echo %realversion | cut -f1,2 -d.).x/rpm-%{realversion}.tar.bz2
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Requires: file nspr nss popt bz2lib db4 lua elfutils
%if "%online" != "true"
Requires: zlib
%endif


# The following two lines are a workaround for an issue seen with gcc4.1.2
Provides: perl(Archive::Tar)
Provides: perl(Specfile)

Patch0: rpm-case-insensitive-sources
Patch1: rpm-add-missing-__fxstat64
Patch2: rpm-fix-glob_pattern_p
Patch3: rpm-remove-strndup
Patch4: rpm-case-insensitive-fixes
Patch5: rpm-allow-empty-buildroot
Patch6: rpm-remove-chroot-check

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
%setup -n %n-%realversion
rm -rf lib/rpmhash.*
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
case %cmsos in
  slc*_ia32)
    export CFLAGS_PLATF="-fPIC -D_FILE_OFFSET_BITS=64"
  ;;
  osx*)
    export CFLAGS_PLATF="-fPIC -fnested-functions"
    export LIBS_PLATF="-liconv"
  ;;
  *)
    export CFLAGS_PLATF="-fPIC"
  ;;
esac 

%if "%online" == "true"
case %cmsos in
  slc5* ) export ZLIB_ROOT=/usr ;;
  * ) export ZLIB_ROOT= ;;
esac 
%endif

USER_CFLAGS="-ggdb -O0"
USER_CXXFLAGS="-ggdb -O0"
#USER_CFLAGS="$USER_CFLAGS -O2"

perl -p -i -e's|-O2|-O0|' ./configure

./configure --prefix %i \
    --with-external-db --disable-python --disable-nls \
    --disable-rpath --with-lua \
    CXXFLAGS="$USER_CXXFLAGS" \
    CFLAGS="$CFLAGS_PLATF $USER_CFLAGS -I$NSPR_ROOT/include/nspr \
            -I$NSS_ROOT/include/nss3 -I$ZLIB_ROOT/include -I$BZ2LIB_ROOT/include \
            -I$DB4_ROOT/include -I$FILE_ROOT/include -I$POPT_ROOT/include \
            -I$LUA_ROOT/include -L$ELFUTILS_ROOT/include" \
    LDFLAGS="-L$NSPR_ROOT/lib -L$NSS_ROOT/lib -L$ZLIB_ROOT/lib -L$DB4_ROOT/lib \
             -L$ELFUTIL_ROOT/lib \
             -L$FILE_ROOT/lib -L$POPT_ROOT/lib -L$BZ2LIB_ROOT/lib -L$LUA_ROOT/lib" \
    CPPFLAGS="-I$NSPR_ROOT/include/nspr \
              -I$ZLIB_ROOT/include -I$BZ2LIB_ROOT/include -I$DB4_ROOT/include \
              -I$FILE_ROOT/include -I$POPT_ROOT/include -I$ELFUTILS_ROOT/include \
              -I$NSS_ROOT/include/nss3 -I$LUA_ROOT/include" \
    LIBS="-lnspr4 -lnss3 -lnssutil3 -lplds4 -lbz2 -lplc4 -lz -lpopt \
          -ldb -llua $LIBS_PLATF"

#FIXME: this does not seem to work and we still get /usr/bin/python in some of the files.
export __PYTHON="/usr/bin/env python"
#perl -p -i -e "s|^.*WITH_SELINUX.*$||;
#               s|-lselinux||;
#" `find . -name \*.in` 

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
               s!^%%_dbpath.*lib/rpm!%%_dbpath %{instroot}/%{cmsplatf}/var/lib/rpm!;
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

# Generates the dependencies-setup.sh/dependencies-setup.csh which is
# automatically sourced by init.sh/init.csh, providing the environment for all
# the dependencies.
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
perl -p -i -e 's|.[{]prefix[}]|%instroot|g' %{i}/lib/rpm/macros

# Remove some of the path macros defined in macros since they could come from
# different places (e.g. from system or from macports) and this would lead to
# problems if a developer with macports builds a bootstrap package set.
for shellUtil in tar cat chgrp chmod chown cp file gpg id make mkdir mv pgp rm rsh sed ssh gzip cpio perl unzip patch grep 
do
    perl -p -i -e "s|^%__$shellUtil\s(.*)|%__$shellUtil       $shellUtil|" %i/lib/rpm/macros
done

ln -sf rpm %i/bin/rpmdb
ln -sf rpm %i/bin/rpmsign
ln -sf rpm %i/bin/rpmverify
ln -sf rpm %i/bin/rpmquery

%post
# do not relocate init.[c]sh as these are done by default from cmsBuild
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g" `grep -I -r %instroot $RPM_INSTALL_PREFIX/%pkgrel | cut -d: -f1 | sort | uniq | grep -v init.csh | grep -v init.sh `
%files
%{i}
%{instroot}/%{cmsplatf}/var/spool/repackage
