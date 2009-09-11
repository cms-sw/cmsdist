### RPM external llvm 2.5
## NOCOMPILER
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

Source0: http://llvm.org/releases/%realversion/%n-gcc-4.2-%realversion.source.tar.gz
Source1: http://llvm.org/releases/%realversion/%n-%realversion.tar.gz
%define gmpVersion 4.2.1
%define mpfrVersion 2.2.1
%define tmpgccVersion 4.2.2
Source2: ftp://ftp.gnu.org/gnu/gmp/gmp-%{gmpVersion}.tar.bz2
Source3: http://www.mpfr.org/mpfr-%{mpfrVersion}/mpfr-%{mpfrVersion}.tar.bz2
Source4: ftp://ftp.fu-berlin.de/unix/gnu/gcc/gcc-%tmpgccVersion/gcc-%tmpgccVersion.tar.bz2

%prep
%setup -T -b 0 -n llvm-gcc4.2-%realversion.source

%if "%cmsos" == "slc4_ia32"
cat << \EOF_CONFIG_GCC >> gcc/config.gcc
# CMS patch to include gcc/config/i386/t-cms when building gcc
tm_file="$tm_file i386/cms.h"
tmake_file="$tmake_file i386/t-cms"
EOF_CONFIG_GCC

cat << \EOF_CMS_H > gcc/config/i386/cms.h
#undef ASM_SPEC
#define ASM_SPEC  "%%{v:-V} %%{Qy:} %%{!Qn:-Qy} %%{n} %%{T} %%{Ym,*} %%{Yd,*} %%{Wa,*:%%*} --32"
#undef CC1_SPEC
#define CC1_SPEC  "%%(cc1_cpu) %%{profile:-p} -m32"
#undef CC1PLUS_SPEC
#define CC1PLUS_SPEC "-m32"
#undef MULTILIB_DEFAULTS
#define MULTILIB_DEFAULTS { "m32" }
EOF_CMS_H

cat << \EOF_T_CMS > gcc/config/i386/t-cms
MULTILIB_OPTIONS = m32
MULTILIB_DIRNAMES = ../lib
MULTILIB_MATCHES = m32=m32
EOF_T_CMS
%endif

%setup -D -T -b 1 -n llvm-%realversion
%setup -D -T -b 2 -n gmp-%{gmpVersion}
%setup -D -T -b 3 -n mpfr-%{mpfrVersion}
%setup -D -T -b 4 -n gcc-%{tmpgccVersion}

%build
%define gcc4opts %{nil}
# Build GMP/MPFR for GCC 4.x
cd ../gmp-%{gmpVersion}
CC="gcc $CCOPTS" ./configure --prefix=%i/tmp/gmp --disable-shared
make %makeprocesses
make install
cd ../mpfr-%{mpfrVersion}
CC="gcc $CCOPTS" ./configure --prefix=%i/tmp/mpfr --with-gmp=%i/tmp/gmp --disable-shared
make %makeprocesses
make install
%define gcc4opts --with-gmp=%i/tmp/gmp --with-mpfr=%i/tmp/mpfr

# build a temporary gcc (c,c++ only) to use for the build 
cd ../gcc-%tmpgccVersion
mkdir -p obj
cd obj
CC="gcc $CCOPTS" \
../configure --prefix=%i/tmp/gcc \
  --enable-languages=c,c++ %gcc4opts --enable-shared
make %makeprocesses bootstrap
make install
find %i/tmp/gcc/lib %i/tmp/gcc/lib32 %i/tmp/gcc/lib64 -name '*.la' -exec rm -f {} \; || true


# Build llvm using the temp gcc
export CC=%i/tmp/gcc/bin/gcc
export CXX=%i/tmp/gcc/bin/g++
export PATH=%i/tmp/gcc/bin:$PATH
export LD_LIBRARY_PATH=%i/tmp/gcc/lib64:%i/tmp/gcc/lib:$LD_LIBRARY_PATH
export GCC_VERSION=%{tmpgccVersion}
export GCC_ROOT=%i/tmp/gcc
export GCC_REVISION=1 
cd ../..
mkdir llvm-objects
cd llvm-objects
../llvm-%realversion/configure --prefix=%i --enable-optimized
make %makeprocesses
make install
# Build the llvm-gcc front-end 
cd ../llvm-gcc4.2-%realversion.source
./configure --prefix=%i %gcc4opts --enable-llvm=`pwd`/../llvm-objects --enable-languages=c,c++
rm GNUmakefile
make %makeprocesses
make install

%install
# Clean up the temporary builds of mpfr and gmp (which had only .a libs)
# and gcc (which should no longer be needed)
rm -fR %i/tmp
# Fix up a perl path
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/bin/llvm-config
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=z>
<client>
 <Environment name=ZLIB_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$ZLIB_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$ZLIB_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
