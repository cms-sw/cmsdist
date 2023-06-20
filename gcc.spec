### RPM external gcc 11.4.1
## USE_COMPILER_VERSION
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
# Use the git repository for fetching the sources. This gives us more control while developing
# a new platform so that we can compile yet to be released versions of the compiler.
# See: https://gcc.gnu.org/viewcvs/gcc/branches/gcc-8-branch/?view=log
%define gccTag d41085966d842e54fd4b528c719ed5af2e51c473
%define gccBranch releases/gcc-11

%define moduleName %{n}-%{realversion}
Source0: git+https://github.com/gcc-mirror/%{n}.git?obj=%{gccBranch}/%{gccTag}&export=%{moduleName}&output=/%{n}-%{realversion}-%{gccTag}.tgz

%define keep_archives true

%define gmpVersion 6.2.1
%define mpfrVersion 4.2.0
%define mpcVersion 1.3.1
%define islVersion 0.26
%define zlibVersion 1.2.13
%define zstdVersion 1.4.5
Source1: https://gmplib.org/download/gmp/gmp-%{gmpVersion}.tar.bz2
Source2: http://www.mpfr.org/mpfr-%{mpfrVersion}/mpfr-%{mpfrVersion}.tar.bz2
Source3: https://ftp.gnu.org/gnu/mpc/mpc-%{mpcVersion}.tar.gz
Source4: https://libisl.sourceforge.io/isl-%{islVersion}.tar.bz2
Source12: http://zlib.net/zlib-%{zlibVersion}.tar.gz
Source13: https://github.com/facebook/zstd/releases/download/v%{zstdVersion}/zstd-%{zstdVersion}.tar.gz

%ifos linux
%define bisonVersion 3.8.2
%define binutilsVersion 2.40
%define elfutilsVersion 0.189
%define m4Version 1.4.19
%define flexVersion 2.6.4
Source7: http://ftp.gnu.org/gnu/bison/bison-%{bisonVersion}.tar.gz
Source8: https://sourceware.org/pub/binutils/releases/binutils-%{binutilsVersion}.tar.bz2
Source9: https://sourceware.org/pub/elfutils/%{elfutilsVersion}/elfutils-%{elfutilsVersion}.tar.bz2
Source10: http://ftp.gnu.org/gnu/m4/m4-%{m4Version}.tar.gz
Source11: https://github.com/westes/flex/releases/download/v%{flexVersion}/flex-%{flexVersion}.tar.gz
%endif

Patch0: gcc-flex-nonfull-path-m4
Patch1: gcc-flex-disable-doc

%prep

%setup -T -b 0 -n %{moduleName}

# Filter out private stuff from RPM requires headers.
cat << \EOF > %{name}-req
#!/bin/sh
%{__find_requires} $* | \
sed -e '/GLIBC_PRIVATE/d'
EOF

%global __find_requires %{_builddir}/%{moduleName}/%{name}-req
chmod +x %{__find_requires}

%ifos linux
%ifarch x86_64
# Hack needed to align sections to 4096 bytes rather than 2MB on 64bit linux
# architectures.  This is done to reduce the amount of address space wasted by
# relocating many libraries. This was done with a linker script before, but
# this approach seems to be more correct.
cat << \EOF_CONFIG_GCC >> gcc/config.gcc
# CMS patch to include gcc/config/i386/cms.h when building gcc
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
%endif
%endif

cat << \EOF_CONFIG_GCC >> gcc/config.gcc
# CMS patch to include gcc/config/general-cms.h when building gcc
tm_file="$tm_file general-cms.h"
EOF_CONFIG_GCC

cat << \EOF_CMS_H > gcc/config/general-cms.h
#undef CC1PLUS_SPEC
#define CC1PLUS_SPEC "-fabi-version=0"
EOF_CMS_H

# GCC prerequisites
%setup -D -T -b 1 -n gmp-%{gmpVersion}
%setup -D -T -b 2 -n mpfr-%{mpfrVersion}
%setup -D -T -b 3 -n mpc-%{mpcVersion}
%setup -D -T -b 4 -n isl-%{islVersion}
%setup -D -T -b 12 -n zlib-%{zlibVersion}
%setup -D -T -b 13 -n zstd-%{zstdVersion}

%ifos linux
%setup -D -T -b 7 -n bison-%{bisonVersion}
%setup -D -T -b 8 -n binutils-%{binutilsVersion}
%setup -D -T -b 9 -n elfutils-%{elfutilsVersion}
%setup -D -T -b 10 -n m4-%{m4Version}
%setup -D -T -b 11 -n flex-%{flexVersion}
%patch0 -p1
%patch1 -p1
%endif

%build
%ifarch darwin
  CC='clang'
  CXX='clang++'
  CPP='clang -E'
  CXXCPP='clang++ -E'
  ADDITIONAL_LANGUAGES=,objc,obj-c++
  CONF_GCC_OS_SPEC=
%else
  CC=gcc
  CXX=c++
  CPP=cpp
  CXXCPP='c++ -E'
  CONF_GCC_OS_SPEC=
%endif

CC="$CC -fPIC"
CXX="$CXX -fPIC"

mkdir -p %{i}/tmp/sw
export PATH=%{i}/tmp/sw/bin:$PATH

# Build zlib (required for compressed debug information)
cd ../zlib-%{zlibVersion}
CONF_FLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1"
%ifarch x86_64
CONF_FLAGS="${CONF_FLAGS} -msse3"
%endif
CFLAGS="${CONF_FLAGS}" ./configure --static --prefix=%{i}/tmp/sw
make %{makeprocesses}
make install

#Build and install zstd static library
make -C ../zstd-%{zstdVersion}/lib %{makeprocesses} \
  install-static install-includes prefix=%{i}/tmp/sw \
  CPPFLAGS="-fPIC" CFLAGS="-fPIC"
%ifos linux
  CONF_BINUTILS_OPTS="--enable-ld=default --enable-lto --enable-plugins --enable-threads"
  CONF_GCC_WITH_LTO="--enable-ld=default --enable-lto"

  CONF_BINUTILS_OPTS="$CONF_BINUTILS_OPTS --enable-gold=yes"
  CONF_GCC_WITH_LTO="$CONF_GCC_WITH_LTO --enable-gold=yes"

  # Build M4 (for building)
  cd ../m4-%{m4Version}
  ./configure --prefix=%{i}/tmp/sw \
              --build=%{_build} --host=%{_host} \
              CC="$CC"
  make %{makeprocesses}
  make install
  hash -r

  # Build Bison (for building)
  cd ../bison-%{bisonVersion}
  ./configure --build=%{_build} --host=%{_host} \
              --prefix=%{i}/tmp/sw CC="$CC"
  make %{makeprocesses}
  make install
  hash -r

  # Build Flex (for building)
  cd ../flex-%{flexVersion}
  ./configure --disable-nls --prefix=%{i}/tmp/sw \
              --enable-static --disable-shared \
              --build=%{_build} --host=%{_host} \
              CC="$CC" CXX="$CXX"
  make %{makeprocesses}
  make install
  hash -r

  # Build elfutils
  cd ../elfutils-%{elfutilsVersion}
  ./configure --disable-static --with-zlib --without-bzlib --without-lzma \
              --disable-libdebuginfod --enable-libdebuginfod=dummy --disable-debuginfod \
              --build=%{_build} --host=%{_host} --program-prefix='eu-' --disable-silent-rules \
              --prefix=%{i} CC="gcc" \
              CPPFLAGS="-I%{i}/tmp/sw/include" LDFLAGS="-L%{i}/tmp/sw/lib"
  make %{makeprocesses}
  make install

%ifarch ppc64le
    CONF_BINUTILS_OPTS="${CONF_BINUTILS_OPTS} --enable-targets=spu --enable-targets=powerpc-linux"
%endif

  # Build binutils
  cd ../binutils-%{binutilsVersion}
  ./configure --disable-static --prefix=%{i} ${CONF_BINUTILS_OPTS} --disable-werror --enable-deterministic-archives \
              --build=%{_build} --host=%{_host} --disable-nls --with-system-zlib --enable-64-bit-bfd \
              CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP" CFLAGS="-I%{i}/include -I%{i}/tmp/sw/include" \
              CXXFLAGS="-I%{i}/include -I%{i}/tmp/sw/include" LDFLAGS="-L%{i}/lib -L%{i}/tmp/sw/lib"
  make %{makeprocesses}
  find . -name Makefile -exec perl -p -i -e 's|LN = ln|LN = cp -p|;s|ln ([^-])|cp -p $1|g' {} \; 
  make install
%endif

# Build GMP
cd ../gmp-%{gmpVersion}
./configure --disable-static --prefix=%{i} --enable-shared --disable-static --enable-cxx \
            --build=%{_build} --host=%{_host} \
            CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
make %{makeprocesses}
make install

# Build MPFR
cd ../mpfr-%{mpfrVersion}
./configure --disable-static --prefix=%{i} --with-gmp=%{i} \
            --build=%{_build} --host=%{_host} \
            CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
make %{makeprocesses}
make install

# Build MPC
cd ../mpc-%{mpcVersion}
./configure --disable-static --prefix=%{i} --with-gmp=%{i} --with-mpfr=%{i} \
            --build=%{_build} --host=%{_host} \
            CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
make %{makeprocesses}
make install

# Build ISL
cd ../isl-%{islVersion}
./configure --disable-static --with-gmp-prefix=%i --prefix=%{i} \
            --build=%{_build} --host=%{_host} \
            CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
make %{makeprocesses}
make install

CONF_GCC_ARCH_SPEC=
%ifarch aarch64
    CONF_GCC_ARCH_SPEC="$CONF_GCC_ARCH_SPEC \
                        --enable-threads=posix --enable-initfini-array --disable-libmpx"
%endif
%ifarch ppc64le
    CONF_GCC_ARCH_SPEC="$CONF_GCC_ARCH_SPEC \
                        --enable-threads=posix --enable-initfini-array \
                        --enable-targets=powerpcle-linux --enable-secureplt --with-long-double-128 \
                        --with-cpu=power8 --with-tune=power8 --disable-libmpx"
%endif

# Build GCC
cd ../%{moduleName}
rm gcc/DEV-PHASE
touch gcc/DEV-PHASE
mkdir -p obj
cd obj
export LD_LIBRARY_PATH=%{i}/lib64:%{i}/lib:$LD_LIBRARY_PATH
../configure --prefix=%{i} --disable-multilib --disable-nls --disable-dssi \
             --enable-languages=c,c++,fortran$ADDITIONAL_LANGUAGES --enable-gnu-indirect-function \
             --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object \
             --enable-plugin --with-linker-hash-style=gnu --enable-linker-build-id \
             $CONF_GCC_OS_SPEC $CONF_GCC_WITH_LTO --with-gmp=%{i} --with-mpfr=%{i} --enable-bootstrap \
             --with-mpc=%{i} --with-isl=%{i} --enable-checking=release \
             --build=%{_build} --host=%{_host} --enable-libstdcxx-time=rt $CONF_GCC_ARCH_SPEC \
             --enable-shared --disable-libgcj \
             --with-zstd=%{i}/tmp/sw \
             CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP" \
             CFLAGS="-I%{i}/tmp/sw/include" CXXFLAGS="-I%{i}/tmp/sw/include" LDFLAGS="-L%{i}/tmp/sw/lib"

make %{makeprocesses} profiledbootstrap

%install
cd %_builddir/%{moduleName}/obj && make install

ln -s gcc %{i}/bin/cc
find %{i}/lib %{i}/lib64 -name '*.la' -exec rm -f {} \; || true

# Remove unneeded documentation, temporary areas, unneeded files.
%define drop_files %{i}/share/{man,info,doc,locale} %{i}/tmp %{i}/lib*/{libstdc++.a,libsupc++.a}
# Strip things people will most likely never debug themself.
%define more_strip %{i}/bin/*{c++,g++,gcc,gfortran,gcov,cpp}*
%define strip_files %{i}/libexec/*/*/*/{cc1,cc1plus,f951,lto1,collect2} %{i}/x86_64*/bin %{i}/lib/lib{mpfr,gmp}* %{more_strip}
%define keep_archives yes
# This avoids having a dependency on the system pkg-config.
rm -rf %{i}/lib/pkg-config

%post
%{relocateConfig}bin/eu-make-debug-archive
%{relocateConfig}etc/profile.d/debuginfod.*sh
%{relocateConfig}lib/gcc/*/%{realversion}/plugin/include/auto-host.h
%{relocateConfig}lib/gcc/*/%{realversion}/plugin/include/configargs.h
%{relocateConfig}lib64/libstdc++*-gdb.py
%{relocateConfig}libexec/gcc/*/%{realversion}/install-tools/mkheaders
%{relocateConfig}libexec/gcc/*/%{realversion}/liblto_plugin.la
for f in $(find $RPM_INSTALL_PREFIX/%{pkgrel}/*/lib/ldscripts -type f) ; do %{relocateCmsFiles} $f || true ; done
