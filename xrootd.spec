### RPM external xrootd 20090727.1318 
Source: http://cmsrep.cern.ch//cmssw/xrootd_src/%n-%{realversion}.tar.gz
Patch0: xrootd-gcc44
Requires: openssl

%prep 
%setup -n %n-%{realversion}
%patch0 -p1

%build
CONFIG_ARGS="--disable-krb4 --with-ssl-incdir=${OPENSSL_ROOT}/include --with-ssl-libdir=${OPENSSL_ROOT}/lib"
case %cmsos in
  slc*_amd64*)
    ./configure.classic x86_64_linux_26 --ccflavour=gccx8664  $CONFIG_ARGS ;;
  slc*_ia32*)
    ./configure.classic i386_linux26 --ccflavour=gcc $CONFIG_ARGS ;;
  *)
   # This is wrong, the arch needs to be added, I think
    ./configure.classic $CONFIG_ARGS ;;
esac

# Workaround for the lack of a 32bit readline-devel rpm for SL4
# Given that the 64bit readline-devel is there, the headers are there,
# the only thing missing is the libreadline.so symlink
case %cmsos in
  slc4*ia32 )
    mkdir tmplib
    ln -s /usr/lib/libreadline.so.4 tmplib/libreadline.so 
    make INCKRB5=-I/usr/include/et LIBKRB5=-lkrb5 LIBREADLINE="-L$PWD/tmplib -lreadline -lcurses"
  ;;
  *)
    make INCKRB5=-I/usr/include/et LIBKRB5=-lkrb5 LIBREADLINE="-lreadline -lcurses"
  ;;
esac


%install
mkdir %i/bin
mkdir %i/lib
mkdir %i/etc
mkdir %i/utils
mkdir %i/src
cp -r bin/arch/* %i/bin
cp -r lib/arch/* %i/lib
[ $(uname) = Darwin ] &&
  for f in %i/lib/*.a; do
    ranlib $f 
  done
cp -r utils/* %i/utils
cp -r etc/* %i/etc
cp -r src/* %i/src
rm -fR %i/bin/CVS %i/lib/CVS %i/utils/CVS %i/etc/CVS %i/src/CVS %i/src/*/CVS
# Need to fix the following in the xrootd CVS
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/etc/XrdOlbMonPerf
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_PreStage
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_MigrPurg
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/fs_stat
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_MonP.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_Lock.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_prep
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_Stage
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_name2name.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_CAlloc.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_Xeq
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/XrdOlbNotify.pm

perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/cleanup.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/loadRTDataToMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonCollector.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/prepareMySQLStats.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonCreateMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonLoadMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonPrepareStats.pl
