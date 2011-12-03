### RPM external xrootd 3.1.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Source: http://xrootd.cern.ch/cgi-bin/cgit.cgi/xrootd/snapshot/%n-%{realversion}.tar.gz
Patch0: xrootd-gcc44
Patch1: xrootd-5.30.00-fix-gcc46
%if "%online" != "true"
Requires: openssl cmake zlib gcc
%endif

%prep 
%setup -n %n-%{realversion}
%patch0 -p1
%patch1 -p1
grep -r -l -e "^#!.*/perl *$" . | xargs perl -p -i -e "s|^#!.*perl *$|#!/usr/bin/env perl|"

%build
mkdir build
cd build
case %cmsos in
  *)
     cmake -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_LIBRARY_PATH=${OPENSSL_ROOT}/lib -DCMAKE_INCLUDE_PATH=${OPENSSL_ROOT}/include ../ ;;
esac

# Workaround to get kerberos compiled in.
case %cmsos in
  *)
    make VERBOSE=1 %{?_smp_mflags}
  ;;
esac


%install
cd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

%define strip_files %i/lib
%define keep_archives true

# need to fix these from xrootd git
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
 <Environment name=LIBDIR  default="$XROOTD_BASE/lib64"></Environment>
</client>
<Runtime name=PATH value="$XROOTD_BASE/bin" type=path>
<Runtime name=LD_LIBRARY_PATH value="$XROOTD_BASE/lib64" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
