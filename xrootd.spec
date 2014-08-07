### RPM external xrootd 4.0.2
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Source: http://xrootd.org/download/v%{realversion}/%{n}-%{realversion}.tar.gz
Patch0: xrootd-3.1.0-fixed-library-location-all-os
Patch1: xrootd-3.1.0-client-send-moninfo
Patch2: xrootd-3.3.3-rc1-add-GetHandle-XrdClientAbs-header
Patch3: xrootd-4.0.2-keep-client-headers

BuildRequires: cmake
%if "%online" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif
Requires: gcc openssl

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -n %n-%{realversion}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

# need to fix these from xrootd git
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/cleanup.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/loadRTDataToMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCollector.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/prepareMySQLStats.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCreateMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonLoadMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonPrepareStats.pl

%build
mkdir build
cd build

# By default xrootd has perl, fuse, krb5, readline, and crypto enabled.
# libfuse and libperl are not produced by CMSDIST.
cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DOPENSSL_ROOT_DIR:PATH=${OPENSSL_ROOT} \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DENABLE_PERL=FALSE \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=FALSE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DCMAKE_CXX_FLAGS="%{cms_cxxflags}"

# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1

%install
cd build
make install
cd ..

%define strip_files %i/lib
%define keep_archives true

