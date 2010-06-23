### RPM external gcc 4.5.0
## BUILDIF case `uname`:`uname -p` in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
## INITENV +PATH LD_LIBRARY_PATH %i/lib/32
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
Source0: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%realversion/%n-%realversion.tar.bz2
# If gcc version >= 4.0.0, we need two additional sources, for gmp and mpfr,
# and we set the fortranCompiler macro (which is going to be used by the 
# --enable-languages option of gcc's configure) to gfortran. 
# Notice that we need to build those twice: once using the system compiler
# and the using the newly built gcc.
%define gmpVersion 4.3.2
%define mpfrVersion 2.4.2
%define mpcVersion 0.8.1
%define pplVersion 0.10.2
%define cloogpplVersion 0.15.9
%define bisonVersion 2.4
Source1: ftp://ftp.gnu.org/gnu/gmp/gmp-%{gmpVersion}.tar.bz2
Source2: http://www.mpfr.org/mpfr-%{mpfrVersion}/mpfr-%{mpfrVersion}.tar.bz2
Source3: http://www.multiprecision.org/mpc/download/mpc-%{mpcVersion}.tar.gz
Source4: http://www.cs.unipr.it/ppl/Download/ftp/releases/0.10.2/ppl-%{pplVersion}.tar.bz2
Source5: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-ppl-%{cloogpplVersion}.tar.gz
Patch0: binutils-2.19.1-fix-gold

%if "%(echo %cmsos | cut -f2 -d_)" == "amd64"
%define binutilsv 2.20.1
Source6: http://ftp.gnu.org/gnu/bison/bison-%{bisonVersion}.tar.bz2
Source7: http://ftp.gnu.org/gnu/binutils/binutils-%binutilsv.tar.bz2
%endif

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%define gcc_major %(echo %realversion | cut -f1 -d.)
%prep
%setup -T -b 0 -n gcc-%realversion 

case %cmsos in
  slc*_ia32 )
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
  ;;
esac

%if "%{?binutilsv:set}" == "set"
%setup -D -T -b 6 -n bison-%{bisonVersion}
%setup -D -T -b 7 -n binutils-%binutilsv
#%%patch0 -p1
case %cmsos in 
  slc*_amd64 )
    # This patches the default linker script to align stuff at 4096 kB boundaries rather 
    # than the default 2MB (MAXPAGESIZE value for x86_64 architecture).
    perl -p -i -e 's|\$[{]MAXPAGESIZE[}]|4096|g;s|\$[{]SEGMENT_SIZE[}]|4096|g' ld/scripttempl/elf.sc
  ;;
esac
%endif

%setup -D -T -b 1 -n gmp-%{gmpVersion}
%setup -D -T -b 2 -n mpfr-%{mpfrVersion}
%setup -D -T -b 3 -n mpc-%{mpcVersion}
%setup -D -T -b 4 -n ppl-%{pplVersion}
%setup -D -T -b 5 -n cloog-ppl-%{cloogpplVersion}

%build
# Set special variables required to build 32-bit executables on 64-bit
# systems.  Note that if the architecture is SLC4/IA32, we may be on a
# 64-bit system and need to produce a 32-bit capable compiler, which
# _itself_ is a 32-bit executable.
case $(uname -m):%{cmsos} in
  *:slc*_ia32 )
    CCOPTS="-fPIC -m32 -Wa,--32" ;;
  * )
    CCOPTS="-fPIC" ;;
esac

USER_CXX=$CCOPTS

# If requested, build our own binutils.  Currently the default is to use
# the system binutils.
%if "%{?binutilsv:set}" == "set"
 cd ../bison-%{bisonVersion}
 CC="gcc $CCOPTS" ./configure --prefix=%i/tmp/bison
 make %makeprocesses
 make install
 export PATH=%i/tmp/bison/bin:$PATH
 cd ../binutils-%{binutilsv}
 ./configure --prefix=%i --enable-gold CC="gcc $CCOPTS"
 make %makeprocesses
 perl -p -i -e 's|LN = ln|LN = cp -p|;s|ln ([^-])|cp -p $1|g' `find . -name Makefile`
 make install
%endif

# Build GMP/MPFR/MPC 
%define gcc4opts %{nil}
%if "%gcc_major" == "4"
cd ../gmp-%{gmpVersion}
./configure --prefix=%i --enable-shared --disable-static --enable-cxx CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
make %makeprocesses
make install

cd ../mpfr-%{mpfrVersion}
./configure --prefix=%i --with-gmp=%i CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
make %makeprocesses
make install

cd ../mpc-%{mpcVersion}
./configure --prefix=%i --with-gmp=%i --with-mpfr=%i CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
make %makeprocesses
make install

cd ../ppl-%{pplVersion}
./configure --prefix=%i CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
make %makeprocesses
make install

cd ../cloog-ppl-%{cloogpplVersion}
./configure --prefix=%i --with-ppl=%i --with-gmp=%i CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
make %makeprocesses
make install

%define gcc4opts --with-gmp=%i --with-mpfr=%i --with-mpc=%i --with-ppl=%i --with-cloog=%i --enable-gold
%endif

# Build the compilers
cd ../gcc-%realversion
mkdir -p obj
cd obj
export LD_LIBRARY_PATH=%i/lib64:%i/lib:$LD_LIBRARY_PATH
../configure --prefix=%i \
  --enable-languages=c,c++,`case %v in 3.*) echo f77;; *) echo fortran;; esac` \
  %gcc4opts --enable-shared CC="gcc $CCOPTS" CXX="c++ $USER_CXX"

make %makeprocesses bootstrap

%install
cd %_builddir/gcc-%{realversion}/obj && make install 

ln -s gcc %i/bin/cc
find %i/lib %i/lib32 %i/lib64 -name '*.la' -exec rm -f {} \; || true
# SCRAM ToolBox toolfile is now geneated by the gcc-toolfile.spec
# so that everything works even in the case "--use-system-compiler"
# option is specified.
