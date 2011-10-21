### RPM external xrootd 5.30.02
%define svntag  %(echo %{realversion} | tr '.' '-')
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Source: svn://root.cern.ch/svn/root/tags/v%{svntag}/net/xrootd/src/xrootd?scheme=http&strategy=export&module=%n-%{realversion}&output=/%n-%{realversion}.tgz
Patch0: xrootd-gcc44
Patch1: xrootd-5.30.00-fix-gcc46
%if "%online" != "true"
Requires: openssl
%endif

%prep 
%setup -n %n-%{realversion}
%patch0 -p1
%patch1 -p1
grep -r -l -e "^#!.*/perl *$" . | xargs perl -p -i -e "s|^#!.*perl *$|#!/usr/bin/env perl|"

%build
CONFIG_ARGS="--disable-krb4 --with-cxx=`which c++` --with-ld=`which c++` --with-ssl-incdir=${OPENSSL_ROOT}/include --with-ssl-libdir=${OPENSSL_ROOT}/lib"
case %cmsos in
  slc*_amd64)
    ./configure.classic x86_64_linux --ccflavour=gccx8664  --enable-krb5 $CONFIG_ARGS --with-krb5=/usr ;;
  slc*_ia32)
    ./configure.classic i386_linux --ccflavour=gcc --enable-krb5 $CONFIG_ARGS --with-krb5=/usr ;;
  *)
   # This is wrong, the arch needs to be added, I think
    ./configure.classic $CONFIG_ARGS ;;
esac

# Workaround to get kerberos compiled in.
case %cmsos in
  slc*)
    make INCKRB5=-I/usr/include/et LIBKRB5=-lkrb5 LIBREADLINE="-lreadline -lcurses" TYPELIBS="-lnsl -lpthread -lrt -ldl -lc -lkrb5"
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
find %i/src -name '*.cc' -exec rm -f {} \;
find %i -name CVS -exec rm -r {} \;
%define strip_files %i/lib
%define keep_archives true

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

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=XrdClient>
<lib name=XrdOuc>
<lib name=XrdNet>
<lib name=XrdSys>
<client>
 <Environment name=XROOTD_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$XROOTD_BASE/src"></Environment>
 <Environment name=LIBDIR  default="$XROOTD_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$XROOTD_BASE/bin" type=path>
<Runtime name=LD_LIBRARY_PATH value="$XROOTD_BASE/lib" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
