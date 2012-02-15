### RPM external gcc 4.5.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib/32
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
Source0: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%realversion/%n-%realversion.tar.bz2
# If gcc version >= 4.0.0, we need two additional sources, for gmp and mpfr.
%define gmpVersion 4.3.2
%define mpfrVersion 2.4.2
%define mpcVersion 0.8.1
Source1: ftp://ftp.gnu.org/gnu/gmp/gmp-%{gmpVersion}.tar.bz2
Source2: http://www.mpfr.org/mpfr-%{mpfrVersion}/mpfr-%{mpfrVersion}.tar.bz2
Source3: http://www.multiprecision.org/mpc/download/mpc-%{mpcVersion}.tar.gz

# For gcc 4.5+ we need the additional tools ppl and cloog.
%define gcc_45plus %(echo %realversion | sed -e 's|4[.][5-9].*|true|')
%if "%{gcc_45plus}" == "true"
%define pplVersion 0.10.2
%define cloogpplVersion 0.15.9
Source4: http://www.cs.unipr.it/ppl/Download/ftp/releases/0.10.2/ppl-%{pplVersion}.tar.bz2
Source5: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-ppl-%{cloogpplVersion}.tar.gz
%endif

# On 64bit Scientific Linux build our own binutils.
%define use_custom_binutils %(echo %cmsos | sed -e 's|slc[0-9]*_amd64|true|')
%if "%use_custom_binutils" == "true"
%define bisonVersion 2.4
%define binutilsv 2.20.1
Source6: http://ftp.gnu.org/gnu/bison/bison-%{bisonVersion}.tar.bz2
Source7: http://ftp.gnu.org/gnu/binutils/binutils-%binutilsv.tar.bz2
%endif

# gcc 4.5+ link time optimization support requires libelf to work. However
# also rpm requires it. In order to have to duplicate dependencies we
# build it in gcc and we pick it up from there also for rpm. Notice that
# libelf does not work on Macosx however this is not a problem until
# we use the system compiler there.
%define isslc %(echo %cmsos | sed -e 's|slc.*|true|')
%define elfutilsVersion 0.131
%if "%isslc" == "true"
Source8: ftp://sources.redhat.com/pub/systemtap/elfutils/elfutils-%{elfutilsVersion}.tar.gz
%endif

%prep
echo "use_custom_binutils: %use_custom_binutils"
%setup -T -b 0 -n gcc-%realversion

case %cmsos in
# Hack to always have -m32 in the 32bit compiler, even when it's built on a 64
# bit architecture.
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
  slc*_amd64 )
# Hack needed to align sections to 4096 bytes rather than 2MB on 64bit linux
# architectures.  This is done to reduce the amount of address space wasted by
# relocating many libraries. This was done with a linker script before, but
# this approach seems to be more correct.
cat << \EOF_CONFIG_GCC >> gcc/config.gcc
# CMS patch to include gcc/config/i386/t-cms when building gcc
tm_file="$tm_file i386/cms.h"
EOF_CONFIG_GCC

cat << \EOF_CMS_H > gcc/config/i386/cms.h
#undef LINK_SPEC
#define LINK_SPEC "%{" SPEC_64 ":-m elf_x86_64} %{" SPEC_32 ":-m elf_i386} \
  %{shared:-shared} \
  %{!shared: \
    %{!static: \
      %{rdynamic:-export-dynamic} \
      %{" SPEC_32 ":%{!dynamic-linker:-dynamic-linker " LINUX_DYNAMIC_LINKER32 "}} \
      %{" SPEC_64 ":%{!dynamic-linker:-dynamic-linker " LINUX_DYNAMIC_LINKER64 "}}} \
    %{static:-static}} -z common-page-size=4096 -z max-page-size=4096"
EOF_CMS_H
  ;;
esac

%if "%{use_custom_binutils}" == "true"
%setup -D -T -b 6 -n bison-%{bisonVersion}
%setup -D -T -b 7 -n binutils-%binutilsv
%endif

# These are required for any gcc 4.x build.
%setup -D -T -b 1 -n gmp-%{gmpVersion}
%setup -D -T -b 2 -n mpfr-%{mpfrVersion}
%setup -D -T -b 3 -n mpc-%{mpcVersion}

# For gcc 4.5 and later we also need the following.
%if "%gcc_45plus" == "true"
%setup -D -T -b 4 -n ppl-%{pplVersion}
%setup -D -T -b 5 -n cloog-ppl-%{cloogpplVersion}
%endif

# These are required by rpm as well, but only on linux.
%if "%isslc" == "true"
%setup -D -T -b 8 -n elfutils-%{elfutilsVersion}
%endif

%build

# Set special variables required to build 32-bit executables on 64-bit
# systems.  Note that if the architecture is SLC4/IA32, we may be on a
# 64-bit system and need to produce a 32-bit capable compiler, which
# _itself_ is a 32-bit executable.
case %{cmsos} in
  slc*_ia32)
    CCOPTS="-fPIC -m32 -Wa,--32" ;;
  *)
    CCOPTS="-fPIC" ;;
esac

# Whenever we build custom binutils we also enable the new linker "gold".
# We do so only if we are using the new gcc 4.5+
if [ "X%use_custom_binutils:%gcc_45plus" = Xtrue:true ] ; then
  CONF_BINUTILS_OPTS="--enable-gold"
fi

USER_CXX=$CCOPTS

# Build libelf.
if [ "X%isslc" = Xtrue ]; then
  cd ../elfutils-%{elfutilsVersion}
  ./configure --prefix=%i CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
  make %makeprocesses
  make install
fi

# If requested, build our own binutils.  Currently the default is to use the
# system binutils on 32bit platforms and our own on 64 bit ones.  
# FIXME: Notice that this copy is actually built using the system compiler, so
# we chances are we will need to rebuild it later on to make sure they get
# linked against our libstdc++ (required by gold).
if [ "X%use_custom_binutils" = Xtrue ]
then
  cd ../bison-%{bisonVersion}
  CC="gcc $CCOPTS" ./configure --prefix=%i/tmp/bison
  make %makeprocesses
  make install
  export PATH=%i/tmp/bison/bin:$PATH
  cd ../binutils-%{binutilsv}
  ./configure --prefix=%i ${CONF_BINUTILS_OPTS} \
              CC="gcc $CCOPTS" CFLAGS="-I%i/include" \
              CXXFLAGS="-I%i/include" LDFLAGS="-L%i/lib"
  make %makeprocesses
  find . -name Makefile -exec perl -p -i -e 's|LN = ln|LN = cp -p|;s|ln ([^-])|cp -p $1|g' {} \; 
  make install
  which ld
fi

# Build GMP/MPFR/MPC
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
CONF_GCC_VERSION_OPTS="--with-gmp=%i --with-mpfr=%i --with-mpc=%i"

# Build additional stuff for gcc 4.5+
if [ "X%gcc_45plus" = Xtrue ]; then
  cd ../ppl-%{pplVersion}
  ./configure --prefix=%i CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
  make %makeprocesses
  make install

  cd ../cloog-ppl-%{cloogpplVersion}
  ./configure --prefix=%i --with-ppl=%i --with-gmp=%i CC="gcc $CCOPTS" CXX="c++ $USER_CXX"
  make %makeprocesses
  make install

  CONF_GCC_VERSION_OPTS="$CONF_GCC_VERSION_OPTS --with-ppl=%i --with-cloog=%i"
fi

# Build the compilers
cd ../gcc-%realversion
mkdir -p obj
cd obj
export LD_LIBRARY_PATH=%i/lib64:%i/lib:$LD_LIBRARY_PATH
../configure --prefix=%i \
  --enable-languages=c,c++,fortran \
  $CONF_GCC_VERSION_OPTS --enable-shared CC="gcc $CCOPTS" CXX="c++ $USER_CXX"

make %makeprocesses bootstrap
make install

%install
cd %_builddir/gcc-%{realversion}/obj && make install 

ln -s gcc %i/bin/cc
find %i/lib %i/lib32 %i/lib64 -name '*.la' -exec rm -f {} \; || true
# SCRAM ToolBox toolfile is now geneated by the gcc-toolfile.spec
# so that everything works even in the case "--use-system-compiler"
# option is specified.
