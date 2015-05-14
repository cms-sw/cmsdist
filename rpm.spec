### RPM external rpm 4.8.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV SET RPM_CONFIGDIR %{i}/lib/rpm
## NOCOMPILER

%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*) echo 1 ;; (*) echo 0 ;; esac)
%define ismac   %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
# Warning! While rpm itself seems to work, at the time of writing it
# does not seem to be possible to build apt-rpm with 
Source: http://rpm.org/releases/rpm-%(echo %realversion | cut -f1,2 -d.).x/rpm-%{realversion}.tar.bz2

Requires: bootstrap-bundle
BuildRequires: gcc

# The following two lines are a workaround for an issue seen with gcc4.1.2
Provides: perl(Archive::Tar)
Provides: perl(Specfile)
# The Module::ScanDeps::DataFeed code is actually contained in perldeps.pl
# but it is dumped out in a temporary file and imported from there, AFAICT.
# For this reason it does not show up as provided by this package.
# In order to work around the problem, we add a fake Provides statement.
Provides: perl(Module::ScanDeps::DataFeed)

Patch0: rpm-4.8.0-case-insensitive-sources
Patch1: rpm-4.8.0-add-missing-__fxstat64
Patch2: rpm-4.8.0-fix-glob_pattern_p
Patch3: rpm-4.8.0-remove-strndup
Patch4: rpm-4.8.0-case-insensitive-fixes
Patch5: rpm-4.8.0-allow-empty-buildroot
Patch6: rpm-4.8.0-remove-chroot-check
Patch7: rpm-4.8.0-fix-missing-libgen
Patch8: rpm-4.8.0-fix-find-provides
Patch9: rpm-4.8.0-increase-line-buffer
Patch10: rpm-4.8.0-increase-macro-buffer
Patch11: rpm-4.8.0-improve-file-deps-speed
Patch12: rpm-4.8.0-fix-fontconfig-provides
Patch13: rpm-4.8.0-fix-find-requires-limit
Patch14: rpm-4.8.0-disable-internal-dependency-generator-libtool
Patch15: rpm-4.8.0-fix-arm
Patch16: rpm-4.8.0-htonll-fix

# Defaults here
%if %ismac
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
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

%build
case %cmsplatf in
  slc*|fc*|*_mic_*)
    CFLAGS_PLATF="-fPIC"
    LIBS_PLATF="-ldl"
  ;;
  osx10[89A]_*_gcc4[789]*)
    export CFLAGS_PLATF="-arch x86_64 -fPIC"
    export LIBS_PLATF="-liconv"
  ;;
  osx*)
    export CFLAGS_PLATF="-arch x86_64 -fPIC -D_FORTIFY_SOURCE=0"
    export LIBS_PLATF="-liconv"
  ;;
  *)
    export CFLAGS_PLATF="-fPIC"
  ;;
esac 

USER_CFLAGS="-ggdb -O0"
USER_CXXFLAGS="-ggdb -O0"
# On SLCx add $GCC_ROOT to various paths because that's where elflib is to be
# found.  Not required (and triggers a warning about missing include path) on
# mac.
case %cmsos in
  slc*)
    OS_CFLAGS="-I$GCC_ROOT/include"
    OS_CXXFLAGS="-I$GCC_ROOT/include"
    OS_CPPFLAGS="-I$GCC_ROOT/include"
    OS_LDFLAGS="-L$GCC_ROOT/lib"
  ;;
esac

perl -p -i -e's|-O2|-O0|' ./configure

# Notice that libelf is now in $GCC_ROOT because also gcc LTO requires it.
./configure --prefix %{i} --build="%{_build}" --host="%{_host}" \
    --with-external-db --disable-python --disable-nls \
    --disable-rpath --with-lua --localstatedir=%{i}/var \
    CXXFLAGS="$USER_CXXFLAGS $OS_CXXFLAGS" \
    CFLAGS="$CFLAGS_PLATF $USER_CFLAGS -I$BOOTSTRAP_BUNDLE_ROOT/include/nspr \
            -I$BOOTSTRAP_BUNDLE_ROOT/include/nss3 -I$BOOTSTRAP_BUNDLE_ROOT/include \
            $OS_CFLAGS" \
    LDFLAGS="-L$BOOTSTRAP_BUNDLE_ROOT/lib $OS_LDFLAGS" \
    CPPFLAGS="-I$BOOTSTRAP_BUNDLE_ROOT/include/nspr \
              -I$BOOTSTRAP_BUNDLE_ROOT/include/nss3 -I$BOOTSTRAP_BUNDLE_ROOT/include \
              $OS_CPPFLAGS" \
    LIBS="-lnspr4 -lnss3 -lnssutil3 -lplds4 -lbz2 -lplc4 -lz -lpopt -llzma \
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
# Remove unneeded documentation
%define drop_files %i/share

# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
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
%{relocateRpmFiles} $(grep -I -r %cmsroot $RPM_INSTALL_PREFIX/%pkgrel | cut -d: -f1 | sort | uniq)
