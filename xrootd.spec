### RPM external xrootd 3.2.4
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc ncurses
%endif

Source: http://xrootd.cern.ch/cgi-bin/cgit.cgi/xrootd/snapshot/%n-%{realversion}.tar.gz
Patch0: xrootd-gcc44
Patch1: xrootd-5.30.00-fix-gcc46
Patch3: xrootd-3.1.0-fixed-library-location-all-os
Patch4: xrootd-3.1.0-client-send-moninfo
Patch5: xrootd-3.1.0-gcc-470-literals-whitespace
Patch6: xrootd-3.1.0-add-GetHandle-XrdClientAbs-header
Patch7: xrootd-3.1.0-narrowing-conversion
Patch8: xrootd-3.2.3-rename-macos-to-apple

%if "%mic" != "true"
BuildRequires: cmake
%endif
%if "%online" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif
Requires: openssl readline

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep 
%setup -n %n-%{realversion}
%patch0 -p1
%patch1 -p1
%patch3 -p0
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

# By default xrootd has perl, fuse, krb5, readline, and crypto enabled.
# libfuse and libperl are not produced by CMSDIST.
%if "%mic" == "true"
 cmake ../ \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE -DCMAKE_EXE_LINKER_FLAGS='-lcrypto -lssl' \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DOPENSSL_ROOT_DIR:PATH=${OPENSSL_ROOT} \
  -DREADLINE_ROOT_DIR=${READLINE_ROOT} \
  -DZLIB_LIBRARY:FILEPATH=${ZLIB_ROOT}/lib/libz.so \
  -DENABLE_PERL=FALSE \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=FALSE \
  -DENABLE_READLINE=FALSE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DCMAKE_CXX_FLAGS="-fPIC -mmic -I${ZLIB_ROOT}/include -I${READLINE_ROOT}/include -I${NCURSES_ROOT}/include -I${NCURSES_ROOT}/include/ncurses -L${NCURSES_ROOT}/lib -L${OPENSSL_ROOT}/lib" \
  -DCMAKE_C_FLAGS="-fPIC -mmic   -I${ZLIB_ROOT}/include -I${READLINE_ROOT}/include -I${NCURSES_ROOT}/include -I${NCURSES_ROOT}/include/ncurses -L${NCURSES_ROOT}/lib -L${OPENSSL_ROOT}/lib" \
  -DCMAKE_CXX_COMPILER=icpc -DCMAKE_C_COMPILER=icc
%else
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
%endif
# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1

%install
cd build
make install
cd ..

%define strip_files %i/lib
%define keep_archives true

