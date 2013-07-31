### RPM external xrootd 3.3.3
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Source: http://xrootd.org/download/v%{realversion}/%{n}-%{realversion}.tar.gz
Patch1: xrootd-5.30.00-fix-gcc46
Patch2: xrootd-3.1.0-fixed-library-location-all-os
Patch3: xrootd-3.1.0-client-send-moninfo
Patch4: xrootd-3.3.3-rc1-add-GetHandle-XrdClientAbs-header
Patch5: xrootd-3.1.0-narrowing-conversion
Patch6: xrootd-3.3.3-rc1-rename-macos-to-apple
Patch7: xrootd-3.3.3-rc1-gcc47
Patch8: xrootd-3.3.3-add-private-headers

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
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1 

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
  -DENABLE_CRYPTO=TRUE \
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

