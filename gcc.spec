### RPM external gcc 4.9.2
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
#Source0: ftp://gcc.gnu.org/pub/gcc/snapshots/4.7.0-RC-20120302/gcc-4.7.0-RC-20120302.tar.bz2
# Use the svn repository for fetching the sources. This gives us more control while developing
# a new platform so that we can compile yet to be released versions of the compiler.
%define gccRevision 223195
%define gccBranch tags/gcc_4_9_2_release

%define moduleName gcc-%(echo %{gccBranch} | tr / _)-%{gccRevision}
Source0: svn://gcc.gnu.org/svn/gcc/%{gccBranch}?module=%{moduleName}&revision=%{gccRevision}&output=/%{moduleName}.tar.gz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)
%define iscpu_marvell %(cat /proc/cpuinfo | grep 'Marvell PJ4Bv7' 2>&1 >/dev/null && echo 1 || echo 0)

%define keep_archives true

%define gmpVersion 6.0.0a
%define mpfrVersion 3.1.2
%define mpcVersion 1.0.2
%define islVersion 0.12.2
%define cloogVersion 0.18.1
%define zlibVersion 1.2.8
Source1: ftp://ftp.gnu.org/gnu/gmp/gmp-%{gmpVersion}.tar.bz2
Source2: http://www.mpfr.org/mpfr-%{mpfrVersion}/mpfr-%{mpfrVersion}.tar.bz2
Source3: http://www.multiprecision.org/mpc/download/mpc-%{mpcVersion}.tar.gz
Source4: ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{islVersion}.tar.bz2
Source5: https://llvm.org/svn/llvm-project/compiler-rt/trunk/lib/asan/scripts/asan_symbolize.py
Source6: http://www.bastoul.net/cloog/pages/download/cloog-%{cloogVersion}.tar.gz
Source12: http://zlib.net/zlib-%{zlibVersion}.tar.gz

%if %islinux
%define bisonVersion 3.0.2
%define binutilsVersion 2.24
%define elfutilsVersion 0.158
%define m4Version 1.4.17
%define flexVersion 2.5.37
Source7: http://ftp.gnu.org/gnu/bison/bison-%{bisonVersion}.tar.gz
Source8: http://ftp.gnu.org/gnu/binutils/binutils-%{binutilsVersion}.tar.bz2
Source9: https://fedorahosted.org/releases/e/l/elfutils/%{elfutilsVersion}/elfutils-%{elfutilsVersion}.tar.bz2
Patch1: https://fedorahosted.org/releases/e/l/elfutils/%{elfutilsVersion}/elfutils-portability.patch
Source10: http://ftp.gnu.org/gnu/m4/m4-%m4Version.tar.gz
Source11: http://garr.dl.sourceforge.net/project/flex/flex-%{flexVersion}.tar.bz2
%endif

%if %isdarwin
Patch2: https://gmplib.org/repo/gmp/raw-rev/1fab0adc5ff7
%endif


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

%if %islinux
%if %isamd64
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
%setup -D -T -b 1 -n gmp-6.0.0
%if %isdarwin 
%patch2 -p1
%endif
%setup -D -T -b 2 -n mpfr-%{mpfrVersion}
%setup -D -T -b 3 -n mpc-%{mpcVersion}
%setup -D -T -b 4 -n isl-%{islVersion}
%setup -D -T -b 6 -n cloog-%{cloogVersion}
%setup -D -T -b 12 -n zlib-%{zlibVersion}

%if %islinux
%setup -D -T -b 7 -n bison-%{bisonVersion}
%setup -D -T -b 8 -n binutils-%{binutilsVersion}
%setup -D -T -b 9 -n elfutils-%{elfutilsVersion}
%patch1 -p1
%setup -D -T -b 10 -n m4-%{m4Version}
%setup -D -T -b 11 -n flex-%{flexVersion}
%endif


%build
%if %isdarwin
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
case %{cmsplatf} in
  *_amd64_*)
    CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
    ./configure --static --prefix=%{i}/tmp/sw
    ;;
  *_armv7hl_*|*_aarch64_*)
    CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
    ./configure --static --prefix=%{i}/tmp/sw
    ;;
  *)
    ./configure --static --prefix=%{i}/tmp/sw
    ;;
esac
make %{makeprocesses}
make install

%if %islinux
  CONF_BINUTILS_OPTS="--enable-gold=yes --enable-ld=default --enable-lto --enable-plugins --enable-threads"
  CONF_GCC_WITH_LTO="--enable-gold=yes --enable-ld=default --enable-lto" # --with-build-config=bootstrap-lto

  # Build M4
  cd ../m4-%{m4Version}
  ./configure --prefix=%{i}/tmp/sw \
              --build=%{_build} --host=%{_host} \
              CC="$CC"
  make %{makeprocesses}
  make install
  hash -r

  # Build Flex
  cd ../flex-%{flexVersion}
  ./configure --disable-nls --prefix=%{i}/tmp/sw \
              --build=%{_build} --host=%{_host} \
              CC="$CC" CXX="$CXX"
  make %{makeprocesses}
  make install
  hash -r

  # Build Bison
  cd ../bison-%{bisonVersion}
  ./configure --build=%{_build} --host=%{_host} \
              --prefix=%{i}/tmp/sw CC="$CC"
  make %{makeprocesses}
  make install
  hash -r

  # Build elfutils
  cd ../elfutils-%{elfutilsVersion}
  ./configure --disable-static --with-zlib --without-bzlib --without-lzma \
              --build=%{_build} --host=%{_host} --program-prefix='eu-'\
              --prefix=%{i} CC="$CC" CPP="$CPP" \
              CFLAGS="-I%{i}/tmp/sw/include" LDFLAGS="-L%{i}/tmp/sw/lib"
  make %{makeprocesses}
  make install

  # Build binutils
  cd ../binutils-%{binutilsVersion}
  ./configure --disable-static --prefix=%{i} ${CONF_BINUTILS_OPTS} --disable-werror \
              --build=%{_build} --host=%{_host} --disable-nls --with-system-zlib --enable-targets=all \
              CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP" CFLAGS="-I%{i}/include -I%{i}/tmp/sw/include" \
              CXXFLAGS="-I%{i}/include -I%{i}/tmp/sw/include" LDFLAGS="-L%{i}/lib -L%{i}/tmp/sw/lib"
  make %{makeprocesses}
  find . -name Makefile -exec perl -p -i -e 's|LN = ln|LN = cp -p|;s|ln ([^-])|cp -p $1|g' {} \; 
  make install
%endif

# Build GMP
cd ../gmp-6.0.0
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

# Build CLooG
cd ../cloog-%{cloogVersion}
./configure --disable-static --prefix=%{i} --with-gmp=system --with-gmp-prefix=%{i} --with-gmp-exec-prefix=%{i} \
            --with-isl=system --with-isl-prefix=%{i} --with-isl-exec-prefix=%{i} \
            --build=%{_build} --host=%{_host} \
            CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP"
make %{makeprocesses}
make install

%if %isarmv7
%if %iscpu_marvell
%define armv7_fpu vfpv3
%else
%define armv7_fpu neon
%endif # iscpu_marvell
%endif # isarmv7

CONF_GCC_ARCH_SPEC=
case %{cmsplatf} in
  *_armv7hl_*)
    CONF_GCC_ARCH_SPEC="$CONF_GCC_ARCH_SPEC \
                        --enable-bootstrap --enable-threads=posix --enable-__cxa_atexit \
                        --disable-libunwind-exceptions --enable-gnu-unique-object \
                        --with-linker-hash-style=gnu --enable-plugin --enable-initfini-array \
                        --enable-linker-build-id --disable-build-with-cxx --disable-build-poststage1-with-cxx \
                        --with-cpu=cortex-a9 --with-tune=cortex-a9 --with-arch=armv7-a \
                        --with-float=hard --with-fpu=%{armv7_fpu} --with-abi=aapcs-linux \
                        --disable-sjlj-exceptions"
    ;;
esac

# Build GCC
cd ../%{moduleName}
rm gcc/DEV-PHASE
touch gcc/DEV-PHASE
mkdir -p obj
cd obj
export LD_LIBRARY_PATH=%{i}/lib64:%{i}/lib:$LD_LIBRARY_PATH
case %{cmsplatf} in 
  osx10*)
../configure --prefix=%{i} --disable-multilib --disable-nls --with-system-zlib --disable-dssi \
             --enable-languages=c,c++,fortran$ADDITIONAL_LANGUAGES \
             --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object \
             --enable-plugin --enable-linker-build-id \
             $CONF_GCC_OS_SPEC $CONF_GCC_WITH_LTO --with-gmp=%{i} --with-mpfr=%{i} \
             --with-mpc=%{i} --with-isl=%{i} --with-cloog=%{i} --enable-checking=release \
             --build=%{_build} --host=%{_host} --enable-libstdcxx-time=rt $CONF_GCC_ARCH_SPEC \
             --enable-shared CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP" \
             CFLAGS="-I%{i}/tmp/sw/include" CXXFLAGS="-I%{i}/tmp/sw/include" LDFLAGS="-L%{i}/tmp/sw/lib"
  ;;
  *)
../configure --prefix=%{i} --disable-multilib --disable-nls --with-system-zlib --disable-dssi \
             --enable-languages=c,c++,fortran$ADDITIONAL_LANGUAGES \
             --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object \
             --enable-plugin --with-linker-hash-style=gnu --enable-linker-build-id \
             $CONF_GCC_OS_SPEC $CONF_GCC_WITH_LTO --with-gmp=%{i} --with-mpfr=%{i} \
             --with-mpc=%{i} --with-isl=%{i} --with-cloog=%{i} --enable-checking=release \
             --build=%{_build} --host=%{_host} --enable-libstdcxx-time=rt $CONF_GCC_ARCH_SPEC \
             --enable-shared CC="$CC" CXX="$CXX" CPP="$CPP" CXXCPP="$CXXCPP" \
             CFLAGS="-I%{i}/tmp/sw/include" CXXFLAGS="-I%{i}/tmp/sw/include" LDFLAGS="-L%{i}/tmp/sw/lib"
  ;;
esac

%if %isamd64
make %{makeprocesses} bootstrap
%else
make %{makeprocesses} bootstrap
%endif
make install

%install
cd %_builddir/%{moduleName}/obj && make install 

ln -s gcc %i/bin/cc
find %i/lib %i/lib64 -name '*.la' -exec rm -f {} \; || true

# Put ASan symbolizer from LLVM into bin directory
cp %SOURCE5 %i/bin/asan_symbolize.py
chmod +x %i/bin/asan_symbolize.py

# Remove unneeded documentation, temporary areas, unneeded files.
%define drop_files %i/share/{man,info,doc,locale} %i/tmp %i/lib*/{libstdc++.a,libsupc++.a}
# Strip things people will most likely never debug themself.
%define more_strip %i/bin/*{c++,g++,gcc,gfortran,gcov,cloog,cpp}*
%define strip_files %i/libexec/*/*/*/{cc1,cc1plus,f951,lto1,collect2} %i/x86_64*/bin %i/lib/lib{mpfr,gmp,cloog}* %more_strip
%define keep_archives yes
# This avoids having a dependency on the system pkg-config.
rm -rf %i/lib/pkg-config
