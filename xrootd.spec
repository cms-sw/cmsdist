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

SOLIB_EXT=so
if [[ %cmsplatf == osx* ]]; then
  SOLIB_EXT=dylib
fi

# By default xrootd has perl, fuse, krb5, readline, and crypto enabled.
# libfuse and libperl are not produced by CMSDIST.
cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%i \
  -DOPENSSL_ROOT_DIR=${OPENSSL_ROOT} \
  -DZLIB_INCLUDE_DIR:PATH=${ZLIB_ROOT}/include \
  -DZLIB_LIBRARY:FILEPATH=${ZLIB_ROOT}/lib/libz.${SOLIB_EXT} \
  -DENABLE_PERL=FALSE \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=TRUE \
  -DENABLE_CRYPTO=TRUE

# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1

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
