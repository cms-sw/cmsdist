### RPM external gcc 4.7.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
#Source0: ftp://gcc.gnu.org/pub/gcc/snapshots/4.7.0-RC-20120302/gcc-4.7.0-RC-20120302.tar.bz2
# Use the svn repository for fetching the sources. This gives us more control while developing
# a new platform so that we can compile yet to be released versions of the compiler.
%define gccRevision 190338
%define gccBranch gcc-%(echo %realversion | cut -f1,2 -d. | tr . _)-branch
Source0: svn://gcc.gnu.org/svn/gcc/branches/%gccBranch?module=gcc-%gccBranch-%gccRevision&revision=%gccRevision&output=/gcc-%gccBranch-%gccRevision.tar.gz

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
%define pplVersion 0.12
%define cloogVersion 0.16.2
Source4: http://bugseng.com/products/ppl/download/ftp/releases/%{pplVersion}/ppl-%{pplVersion}.tar.bz2
Source5: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloogVersion}.tar.gz
%endif

# On 64bit Scientific Linux build our own binutils.
# Notice that since we don't support building 32bit nor slc4 anymore.
%define use_custom_binutils %(case %cmsos in (slc*) echo true ;; (*) echo false ;; esac)
%if "%use_custom_binutils" == "true"
%define bisonVersion 2.5
Source6: http://ftp.gnu.org/gnu/bison/bison-%{bisonVersion}.tar.bz2
%define binutilsv 2.22
Source7: http://ftp.gnu.org/gnu/binutils/binutils-%binutilsv.tar.bz2
#Source7: http://cmsrep.cern.ch/cmssw/binutils-mirror/binutils-%binutilsv.tar.bz2
#Source7: http://www.kernel.org/pub/linux/devel/binutils/binutils-%binutilsv.tar.bz2
%endif

# gcc 4.5+ link time optimization support requires libelf to work. However
# also rpm requires it. In order to have to duplicate dependencies we
# build it in gcc and we pick it up from there also for rpm. Notice that
# libelf does not work on Macosx however this is not a problem until
# we use the system compiler there.
%define isslc %(case %cmsos in (slc*) echo true ;; (*) echo false ;; esac)
%define elfutilsVersion 0.153
%if "%isslc" == "true"
Source8: https://fedorahosted.org/releases/e/l/elfutils/%{elfutilsVersion}/elfutils-%{elfutilsVersion}.tar.bz2
%endif
Patch2: https://fedorahosted.org/releases/e/l/elfutils/0.153/elfutils-portability.patch

%prep
echo "use_custom_binutils: %use_custom_binutils"
%setup -T -b 0 -n gcc-%gccBranch-%gccRevision

case %cmsos in
  slc*_gcc4[0-6]*)
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
slc*)
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
      %{" SPEC_32 ":%{!dynamic-linker:-dynamic-linker " GNU_USER_DYNAMIC_LINKER32 "}} \
      %{" SPEC_64 ":%{!dynamic-linker:-dynamic-linker " GNU_USER_DYNAMIC_LINKER64 "}}} \
    %{static:-static}} -z common-page-size=4096 -z max-page-size=4096"
EOF_CMS_H
  ;;
esac

case %cmsos in
  slc*_corei7)
cat << \EOF_CMS_H >> gcc/config/i386/cms.h
#undef ASM_SPEC
#define ASM_SPEC  "%%{v:-V} %%{Qy:} %%{!Qn:-Qy} %%{n} %%{T} %%{Ym,*} %%{Yd,*} %%{Wa,*:%%*} -march=corei7 -mtune=corei7"
#undef CC1_SPEC
#define CC1_SPEC  "%%(cc1_cpu) %%{profile:-p} -march=corei7 -mtune=corei7"
#undef CC1PLUS_SPEC
#define CC1PLUS_SPEC "-march=corei7"
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
  osx10[0-6]*)
    CC='/usr/bin/gcc-4.2'
    CXX='/usr/bin/c++-4.2'
    CPP='/usr/bin/cpp-4.2'
    CXXCPP='/usr/bin/c++-4.2 -E'
    ADDITIONAL_LANGUAGES=,objc,obj-c++

    # Apparently must emulate apple compiler even if we build
    # full chain ourselves, as things come in via system libs.
    #  - http://newartisans.com/2009/10/a-c-gotcha-on-snow-leopard/
    #  - http://gcc.gnu.org/bugzilla/show_bug.cgi?id=41645
    #  - http://trac.macports.org/ticket/25205 (and 22234)
    CONF_GCC_OS_SPEC=--enable-fully-dynamic-string
  ;;
  osx*)
    # Depend on XCode provided /usr snapshot
    export PATH=/Developer/usr/bin:$PATH
    CC='/Developer/usr/bin/clang'
    CXX='/Developer/usr/bin/clang++'
    CPP='/Developer/usr/bin/clang -E'
    CXXCPP='/Developer/usr/bin/clang++ -E'
    ADDITIONAL_LANGUAGES=,objc,obj-c++
    
    # Disable for Lion (10.7.X) otherwise ld will fail on libgfortran.la
    #CONF_GCC_OS_SPEC=--enable-fully-dynamic-string
  ;;
  *)
    CC=gcc
    CXX=c++
    CPP=cpp
    CXXCPP='c++ -E'
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
  ./configure --disable-static --without-zlib \
              --without-bzlib --without-lzma \
              --prefix=%i CC="$CC" CXX="$CXX -Wno-strict-aliasing" CPP="$CPP" CXXCPP="$CXXCPP"
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
              CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP" CFLAGS="-I%i/include" \
              CXXFLAGS="-I%i/include" LDFLAGS="-L%i/lib"
  make %makeprocesses
  find . -name Makefile -exec perl -p -i -e 's|LN = ln|LN = cp -p|;s|ln ([^-])|cp -p $1|g' {} \; 
  make install
  which ld
fi

# Build GMP/MPFR/MPC
cd ../gmp-%{gmpVersion}
./configure --disable-static --prefix=%i --enable-shared --disable-static --enable-cxx \
  CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
make %makeprocesses
make install

cd ../mpfr-%{mpfrVersion}
./configure --disable-static --prefix=%i --with-gmp=%i CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
make %makeprocesses
make install

cd ../mpc-%{mpcVersion}
./configure --disable-static --prefix=%i --with-gmp=%i --with-mpfr=%i CC="$CC" CXX="$CXX" \
  CPP="$CPP" CXXCPP="$CXXCPP"
make %makeprocesses
make install
CONF_GCC_VERSION_OPTS="--with-gmp=%i --with-mpfr=%i --with-mpc=%i"

# Build additional stuff for gcc 4.5+
if [ "X%gcc_45plus" = Xtrue ]; then
  cd ../ppl-%{pplVersion}
  ./configure --disable-static --with-gmp=%i --with-cxxflags="-I%i/include" \
    --enable-interfaces=c --prefix=%i CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP" \
    LDFLAGS="-L%i/lib"
  make %makeprocesses
  make install

  cd ../cloog-%{cloogVersion}
  ./configure --disable-static --prefix=%i --with-ppl=%i --with-gmp-prefix=%i CC="$CC" \
    CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
  make %makeprocesses
  make install

  CONF_GCC_VERSION_OPTS="$CONF_GCC_VERSION_OPTS --with-ppl=%i --with-cloog=%i --enable-cloog-backend=isl"
fi

# Build the compilers
cd ../gcc-%gccBranch-%gccRevision
mkdir -p obj
cd obj
export LD_LIBRARY_PATH=%i/lib64:%i/lib:$LD_LIBRARY_PATH
../configure --prefix=%i --disable-multilib --disable-nls \
  --enable-languages=c,c++,fortran$ADDITIONAL_LANGUAGES \
  $CONF_GCC_OS_SPEC $CONF_GCC_WITH_LTO $CONF_GCC_VERSION_OPTS \
  --enable-shared CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"

make %makeprocesses bootstrap
make install

%install
cd %_builddir/gcc-%gccBranch-%gccRevision/obj && make install 

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
