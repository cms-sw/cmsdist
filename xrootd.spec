### RPM external xrootd 4.0.4
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
%define tag 333bc986604f0e127ffd705be2abb491a1b443b7
%define branch cms/v4.0.4
%define github_user cms-externals
Source: git+https://github.com/%github_user/xrootd.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: zlib
Requires: openssl libevent

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -n %n-%{realversion}

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
  -DZLIB_LIBRARY=${ZLIB_ROOT}/lib/libz.so \
  -DZLIB_INCLUDE_DIR=${ZLIB_ROOT}/include \
  -DOPENSSL_ROOT_DIR=${OPENSSL_ROOT} \
  -DLIBEVENT_LIB=${LIBEVENT_ROOT}/lib/libevent.so \
  -DLIBEVENT_INCLUDE_DIR=${LIBEVENT_ROOT}/include \
  -DLIBEVENTPTHREADS_LIB=${LIBEVENT_ROOT}/lib/libevent_pthreads.so \
  -DLIBEVENTPTHREADS_INCLUDE_DIR=${LIBEVENT_ROOT}/include \
  -DENABLE_FUSE=0 \
  -DENABLE_KRB5=1 \
  -DENABLE_READLINE=0 \
  -DENABLE_CRYPTO=1 \
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

