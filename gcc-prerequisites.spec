### RPM external gcc-prerequisites 1.0
## NOCOMPILER
AutoReqProv: no
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

%install
echo "Package every thing under %{i}"
#backup etc/profile.d
[ ! -d %{i}/etc/profile.d ] || mv %{i}/etc/profile.d %{i}/etc/profile.d.gcc
