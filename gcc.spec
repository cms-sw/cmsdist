### RPM external gcc 4.6.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
Source0: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%realversion/%n-%realversion.tar.bz2

%define keep_archives true

# For gcc version >= 4.0.0, a number of additional sources are needed.
%define gmpVersion 5.0.2
%define mpfrVersion 3.0.1 
%define mpcVersion 0.9
Source1: ftp://ftp.gnu.org/gnu/gmp/gmp-%{gmpVersion}.tar.bz2
Source2: http://www.mpfr.org/mpfr-%{mpfrVersion}/mpfr-%{mpfrVersion}.tar.bz2
Source3: http://www.multiprecision.org/mpc/download/mpc-%{mpcVersion}.tar.gz

# For gcc 4.5+ we need the additional tools ppl and cloog.
%define gcc_45plus %(echo %realversion | sed -e 's|4[.][5-9].*|true|')
%if "%{gcc_45plus}" == "true"
%define pplVersion 0.11.2
%define cloogVersion 0.16.2
Source4: http://bugseng.com/products/ppl/download/ftp/releases/%{pplVersion}/ppl-%{pplVersion}.tar.bz2
Source5: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloogVersion}.tar.gz
%endif

# On 64bit Scientific Linux build our own binutils.
%define use_custom_binutils %(echo %cmsos | sed -e 's|slc[0-9]*_amd64|true|')
%if "%use_custom_binutils" == "true"
%define bisonVersion 2.4
Source6: http://ftp.gnu.org/gnu/bison/bison-%{bisonVersion}.tar.bz2
%define binutilsv 2.21.1
Source7: http://ftp.gnu.org/gnu/binutils/binutils-%binutilsv.tar.bz2
#Source7: http://cmsrep.cern.ch/cmssw/binutils-mirror/binutils-%binutilsv.tar.bz2
#Source7: http://www.kernel.org/pub/linux/devel/binutils/binutils-%binutilsv.tar.bz2
%endif

# gcc 4.5+ link time optimization support requires libelf to work. However
# also rpm requires it. In order to have to duplicate dependencies we
# build it in gcc and we pick it up from there also for rpm. Notice that
# libelf does not work on Macosx however this is not a problem until
# we use the system compiler there.
%define isslc %(echo %cmsos | sed -e 's|slc.*|true|')
%define elfutilsVersion 0.153
%if "%isslc" == "true"
Source8: https://fedorahosted.org/releases/e/l/elfutils/%{elfutilsVersion}/elfutils-%{elfutilsVersion}.tar.bz2
%endif
Patch0: gcc-4.6.1-ignore-arch-flags-macosx
# See http://gcc.gnu.org/bugzilla/show_bug.cgi?id=49540
Patch1: gcc-4.6.1-fix-gfortran-regression
Patch2: https://fedorahosted.org/releases/e/l/elfutils/%{elfutilsVersion}/elfutils-portability.patch

%prep
echo "use_custom_binutils: %use_custom_binutils"
%setup -T -b 0 -n gcc-%realversion
%if "%gcc_45plus" == "true"
# Get the macosx build to accept -arch, -F options like the official Apple one.
# Notice that  patch command have to stay on a single line.
case %cmsos in
  osx*)
%patch0 -p1 
  ;;
esac
%patch1 -p0
%endif

case %cmsos in
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
%setup -D -T -b 5 -n cloog-%{cloogVersion}
%endif

# These are required by rpm as well, but only on linux.
%if "%isslc" == "true"
%setup -D -T -b 8 -n elfutils-%{elfutilsVersion}
%patch2 -p1
%endif

%build
# On mac we need to use gcc-proper, not gcc-llvm
case %{cmsos} in
  osx*)
    CC=/usr/bin/gcc-4.2
    CXX=/usr/bin/c++-4.2
    CPP=/usr/bin/cpp-4.2
    ADDITIONAL_LANGUAGES=,objc,obj-c++

    # Apparently must emulate apple compiler even if we build
    # full chain ourselves, as things come in via system libs.
    #  - http://newartisans.com/2009/10/a-c-gotcha-on-snow-leopard/
    #  - http://gcc.gnu.org/bugzilla/show_bug.cgi?id=41645
    #  - http://trac.macports.org/ticket/25205 (and 22234)
    CONF_GCC_OS_SPEC=--enable-fully-dynamic-string
  ;;
  *)
    CC=gcc
    CXX=c++
    CPP=cpp
    CONF_GCC_OS_SPEC=
  ;;
esac

CC="$CC -fPIC"
CXX="$CXX -fPIC"

# Whenever we build custom binutils we also enable the new linker "gold".
# We do so only if we are using the new gcc 4.5+
if [ "X%use_custom_binutils:%gcc_45plus" = Xtrue:true ] ; then
  CONF_BINUTILS_OPTS="--enable-gold=default --enable-lto --enable-plugins --enable-threads"
  CONF_GCC_WITH_LTO="--enable-gold=yes --enable-lto" # --with-build-config=bootstrap-lto
fi

# Build libelf.
if [ "X%isslc" = Xtrue ]; then
  cd ../elfutils-%{elfutilsVersion}
  ./configure --disable-static --prefix=%i CC="$CC" CXX="$CXX" CPP="$CPP"
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
  CC="$CC" ./configure --prefix=%i/tmp/bison
  make %makeprocesses
  make install
  export PATH=%i/tmp/bison/bin:$PATH
  cd ../binutils-%{binutilsv}
  # Try to avoid dependency on makeinfo by forcing make not
  # to build the documentation.
  perl -p -i -e 's|SUBDIRS = .*|SUBDIRS =|' bfd/Makefile.in binutils/Makefile.in gas/Makefile.in
  perl -p -i -e 's|all: info|all:|' etc/Makefile.in
  perl -p -i -e 's|TEXINFOS =.*|TEXINFOS =|;s|INFO_DEPS =.*|INFO_DEPS =|' gprof/Makefile.in
  perl -p -i -e 's|man_MANS =.*|man_MANS =|' gprof/Makefile.in
  perl -p -i -e 's|INFO_DEPS =.*|INFO_DEPS =|' ld/Makefile.in
  perl -p -i -e 's|INFOFILES =.*|INFOFILES =|' etc/Makefile.in
  perl -p -i -e 's|DVIFILES =.*|DVIFILES =|' etc/Makefile.in
  perl -p -i -e 's|PDFFILES =.*|PDFFILES =|' etc/Makefile.in
  perl -p -i -e 's|HTMLFILES =.*|HTMLFILES =|' etc/Makefile.in        

  ./configure --disable-static --prefix=%i ${CONF_BINUTILS_OPTS} --disable-werror \
              CC="$CC" CXX="$CXX" CPP="$CPP" CFLAGS="-I%i/include" \
              CXXFLAGS="-I%i/include" LDFLAGS="-L%i/lib"
  make %makeprocesses
  find . -name Makefile -exec perl -p -i -e 's|LN = ln|LN = cp -p|;s|ln ([^-])|cp -p $1|g' {} \; 
  make install
  which ld
fi

# Build GMP/MPFR/MPC
cd ../gmp-%{gmpVersion}
./configure --disable-static --prefix=%i --enable-shared --disable-static --enable-cxx CC="$CC" CXX="$CXX" CPP="$CPP"
make %makeprocesses
make install

cd ../mpfr-%{mpfrVersion}
./configure --disable-static --prefix=%i --with-gmp=%i CC="$CC" CXX="$CXX" CPP="$CPP"
make %makeprocesses
make install

cd ../mpc-%{mpcVersion}
./configure --disable-static --prefix=%i --with-gmp=%i --with-mpfr=%i CC="$CC" CXX="$CXX" CPP="$CPP"
make %makeprocesses
make install
CONF_GCC_VERSION_OPTS="--with-gmp=%i --with-mpfr=%i --with-mpc=%i"

# Build additional stuff for gcc 4.5+
if [ "X%gcc_45plus" = Xtrue ]; then
  cd ../ppl-%{pplVersion}
  ./configure --disable-static --with-gmp-prefix=%i --with-cxxflags="-I%i/include" --enable-interfaces=c --prefix=%i CC="$CC" CXX="$CXX" CPP="$CPP" LDFLAGS="-L%i/lib"
  make %makeprocesses
  make install

  cd ../cloog-%{cloogVersion}
  ./configure --disable-static --prefix=%i --with-ppl=%i --with-gmp-prefix=%i CC="$CC" CXX="$CXX" CPP="$CPP"
  make %makeprocesses
  make install

  CONF_GCC_VERSION_OPTS="$CONF_GCC_VERSION_OPTS --with-ppl=%i --with-cloog=%i --enable-cloog-backend=isl"
fi

# Build the compilers
cd ../gcc-%realversion
mkdir -p obj
cd obj
export LD_LIBRARY_PATH=%i/lib64:%i/lib:$LD_LIBRARY_PATH
../configure --prefix=%i --disable-multilib --disable-nls \
  --enable-languages=c,c++,fortran$ADDITIONAL_LANGUAGES \
  $CONF_GCC_OS_SPEC $CONF_GCC_WITH_LTO $CONF_GCC_VERSION_OPTS \
  --enable-shared CC="$CC" CXX="$CXX" CPP="$CPP"

make %makeprocesses bootstrap
make install

%install
cd %_builddir/gcc-%{realversion}/obj && make install 

ln -s gcc %i/bin/cc
find %i/lib %i/lib64 -name '*.la' -exec rm -f {} \; || true

# Remove unneeded documentation, temporary areas, unneeded files.
%define drop_files %i/share/{man,info,doc,locale} %i/tmp %i/lib*/{libstdc++.a,libsupc++.a}
# Strip things people will most likely never debug themself.
%define more_strip %i/bin/*{c++,g++,gcc,gfortran,gcov,ppl,cloog,cpp}*
%define strip_files %i/libexec/*/*/*/{cc1,cc1plus,f951,lto1,collect2} %i/x86_64*/bin %i/lib/lib{mpfr,ppl,gmp,cloog}* %more_strip
%define keep_archives yes
# This avoids having a dependency on the system pkg-config.
rm -rf %i/lib/pkg-config
