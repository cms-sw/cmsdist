### RPM external gcc 12.3.1
## USE_COMPILER_VERSION
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
# Use the git repository for fetching the sources. This gives us more control while developing
# a new platform so that we can compile yet to be released versions of the compiler.
# See: https://gcc.gnu.org/viewcvs/gcc/branches/gcc-8-branch/?view=log
BuildRequires: gcc-prerequisites
%define gccTag b76c4656631977ccf5119bd326df5e03d26f66ac
%define gccBranch releases/gcc-12

%define moduleName %{n}-%{realversion}
Source0: git+https://github.com/gcc-mirror/%{n}.git?obj=%{gccBranch}/%{gccTag}&export=%{moduleName}&output=/%{n}-%{realversion}-%{gccTag}.tgz

%define keep_archives true

#Fix for array-bound
Source1: https://github.com/gcc-mirror/gcc/commit/49ba4fdeb648c149fa7d964ba812084262c3d06f.patch

%prep

%setup -T -b 0 -n %{moduleName}
patch -p1 < %{_sourcedir}/49ba4fdeb648c149fa7d964ba812084262c3d06f.patch

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

mkdir -p %{i}
rsync -a ${GCC_PREREQUISITES_ROOT}/ %{i}/
if [ -d %{i}/etc/profile.d ] ; then
  rm -rf %{i}/etc/profile.d
  [ -d %{i}/etc/profile.d.gcc ] && mv %{i}/etc/profile.d.gcc %{i}/etc/profile.d
fi
export PATH=%{i}/tmp/sw/bin:$PATH

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
             -enable-libstdcxx-backtrace=yes \
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
