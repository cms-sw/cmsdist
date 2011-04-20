### RPM cms llvm-gcc-toolfile 11.0

Requires: llvm
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif
Source: none

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%else
Requires: gcc
%endif

%prep
%build
%install
mkdir -p %i/etc/scram.d

export LLVM_PATH
export LLVM_ROOT
export LLVM_VERSION

# Determine the GCC_ROOT if "use system compiler is used.  We still need this
# because we need to pick up libstdc++ from the gcc installation since clang
# does not ship its own and because clang does not provide a fortran compiler.
if [ "X$GCC_ROOT" = X ]
then
    export GCC_PATH=`which gcc` || exit 1
    export GCC_ROOT=`echo $GCC_PATH | sed -e 's|/bin/gcc||'`
    export GCC_VERSION=`gcc -v 2>&1 | grep "gcc version" | sed 's|[^0-9]*\([0-9].[0-9].[0-9]\).*|\1|'` || exit 1
    export G77_ROOT=$GFORTRAN_MACOSX_ROOT
else
    export GCC_PATH
    export GCC_ROOT
    export GCC_VERSION
    export G77_ROOT=$GCC_ROOT
fi
export GCC_REALVERSION=`echo $GCC_VERSION | sed -e's|-.*||'`
export COMPILER_VERSION=`echo $LLVM_VERSION`
export COMPILER_VERSION_MAJOR=`echo $LLVM_VERSION | sed -e 's|\([0-9]\).*|\1|'`
export COMPILER_VERSION_MINOR=`echo $LLVM_VERSION | sed -e 's|[0-9].\([0-9]\).*|\1|'`

export GCC_ARCH=$(basename $(dirname `find $GCC_ROOT/include -mindepth 4 -maxdepth 4 -name bits`))

# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler.xml
  <tool name="cxxcompiler" version="@LLVM_VERSION@" type="compiler">
    <client>
      <environment name="CXXCOMPILER_BASE" default="@LLVM_ROOT@"/>
      <environment name="GCCBINDIR" default="$CXXCOMPILER_BASE/bin"/>
      <environment name="CXX" value="$GCCBINDIR/clang++@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags SCRAM_COMPILER_NAME="clang@COMPILER_VERSION@"/>
    <flags CCCOMPILER="clang@COMPILER_VERSION_MAJOR@"/>
    <flags MODULEFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@"/>
    <flags CXXDEBUGFLAG="-g"/>
    <flags CPPDEFINES="GNU_GCC"/>
    <flags CPPDEFINES="_GNU_SOURCE"/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC"/>
    <flags CPPFLAGS="-I@GCC_ROOT@/include/c++/@GCC_REALVERSION@"/>
    <flags CPPFLAGS="-I@GCC_ROOT@/include/c++/@GCC_REALVERSION@/@GCC_ARCH@"/>
    <flags CPPFLAGS="-I@GCC_ROOT@/include/c++/@GCC_REALVERSION@/backward"/>
    <flags CXXFLAGS="-O2 -ansi -pthread -pipe"/>
    <flags CXXFLAGS="@ARCH_CXXFLAGS@ @COMPILER_CXXFLAGS@"/>
    <flags CXXFLAGS="-fmessage-length=0 -ftemplate-depth-300"/>
    # -Wno-non-template-friend removed since it's not supported, yet, by llvm.
    <flags CXXFLAGS="-Wall -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wsign-compare -Wno-deprecated -Werror=return-type -Werror=missing-braces -Werror=unused-value -Werror=address -Werror=format -Werror=write-strings -Werror=strict-overflow -fdiagnostics-show-option"/>
    <flags LDFLAGS="@OS_LDFLAGS@ -L@GCC_ROOT@/lib64"/>
    <flags CXXSHAREDFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@"/>
    <flags SHAREDSUFFIX="@OS_SHAREDSUFFIX@"/>
    <flags LD_UNIT="@OS_LD_UNIT@ @ARCH_LD_UNIT@"/>
    <flags SCRAM_LANGUAGE_TYPE="C++"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="PATH" value="$CXXCOMPILER_BASE/bin" type="path"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="@GCC_ROOT@/@ARCH_LIB64DIR@" type="path"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="@GCC_ROOT@/lib" type="path"/>
    <runtime name="COMPILER_RUNTIME_OBJECTS" value="@GCC_ROOT@/lib/gcc/@GCC_ARCH@/@GCC_REALVERSION@"/>
    <runtime name="PATH" value="@GCC_ROOT@/bin" type="path"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler.xml
  <tool name="ccompiler" version="@LLVM_VERSION@" type="compiler">
    <client>
      <environment name="CCOMPILER_BASE" default="@LLVM_ROOT@"/>
      <environment name="GCCBINDIR" value="$CCOMPILER_BASE/bin"/>
      <environment name="CC" value="$GCCBINDIR/clang@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags CDEBUGFLAG="-g"/>
    <flags CSHAREDOBJECTFLAGS="-fPIC"/>
    <flags CFLAGS="-pthread"/>
    <flags CFLAGS="-O2"/>
    <flags LDFLAGS="@OS_LDFLAGS@ -L@GCC_ROOT@/lib64"/>
    <flags CSHAREDFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@"/>
    <flags SCRAM_COMPILER_NAME="clangc@COMPILER_VERSION@"/>
    <flags SCRAM_LANGUAGE_TYPE="C"/>
  </tool>
EOF_TOOLFILE

# Notice that on OSX we have a LIBDIR defined for f77compiler because gcc C++
# compiler (which comes from the system) does not know about where to find
# libgfortran. 
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler.xml
  <tool name="f77compiler" version="@GCC_VERSION@" type="compiler">
    <lib name="gfortran"/>
    <lib name="m"/>
    <client>
      <environment name="F77COMPILER_BASE" default="@G77_ROOT@"/>
      <environment name="FC" default="$F77COMPILER_BASE/bin/gfortran"/>
      @ARCH_FORTRAN_LIBDIR@
    </client>
    <flags SCRAM_COMPILER_NAME="clang@COMPILER_VERSION@"/>
    <flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2"/>
    <flags FCO2FLAG="-O2"/>
    <flags FCOPTIMISED="-O2"/>
    <flags FCDEBUGFLAG="-g"/>
    <flags FCSHAREDOBJECTFLAGS="-fPIC"/>
    <flags SCRAM_LANGUAGE_TYPE="FORTRAN"/>
  </tool>
EOF_TOOLFILE

# NON-empty defaults
export COMPILER_EXEC_NAME="clang++"

# First of all handle OS specific options.
case %cmsplatf in
  slc* )
    export OS_SHAREDFLAGS="-shared -Wl,-E"
    export OS_SHAREDSUFFIX="so"
    export OS_LDFLAGS="-Wl,-E -Wl,--hash-style=gnu"
    export OS_RUNTIME_LDPATH_NAME="LD_LIBRARY_PATH"
  ;;
  osx* )
    export OS_SHAREDFLAGS="-shared -dynamic -single_module"
    export OS_SHAREDSUFFIX="dylib"
    export OS_LDFLAGS="-Wl,-commons -Wl,use_dylibs"
    export OS_RUNTIME_LDPATH_NAME="DYLD_LIBRARY_PATH"
  ;;
esac

# Then handle OS + architecture specific options (maybe we should enable more
# aggressive optimizations for amd64 as well??)
case %cmsplatf in
  osx*_ia32_* )
    export ARCH_CXXFLAGS="-arch i386"
    export ARCH_SHAREDFLAGS="-arch i386"
    export ARCH_LIB64DIR="lib"
    export ARCH_FORTRAN_LIBDIR='<environment name="LIBDIR" default="$F77COMPILER_BASE/lib/gcc/i686-apple-darwin10/4.2.1"/>'
  ;;
  osx*_amd64_* )
    export ARCH_CXXFLAGS="-arch x86_64"
    export ARCH_SHAREDFLAGS="-arch x86_64"
    export ARCH_LIB64DIR="lib"
    export ARCH_FORTRAN_LIBDIR='<environment name="LIBDIR" default="$F77COMPILER_BASE/lib/gcc/i686-apple-darwin10/4.2.1/x86_64"/>'
  ;;
  osx*_ppc32_* )
    export ARCH_CXXFLAGS="-arch ppc"
    export ARCH_SHAREDFLAGS="-arch ppc"
    export ARCH_LIB64DIR="lib"
  ;;
  slc*_amd64_* )
    # For some reason on mac, some of the header do not compile if this is
    # defined.  Ignore for now.
    export ARCH_CXXFLAGS="-Werror=overflow"
    export ARCH_LIB64DIR="lib64"
    export ARCH_LD_UNIT="-r -m elf_x86_64"
  ;;
  slc*_ia32_* )
    # For some reason on mac, some of the header do not compile if this is
    # defined.  Ignore for now.
    export ARCH_CXXFLAGS="-Werror=overflow"
    export ARCH_LIB64DIR="lib"
    export ARCH_LD_UNIT="-r -m elf_i386"
  ;;
  *) 
    echo "Unsupported."
    exit 1
  ;;
esac

# Then handle compiler specific options. E.g. enable
# optimizations as they become available in gcc.
COMPILER_CXXFLAGS=
case %cmsplatf in
   *_gcc4[56789]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS"
     F77_MMD="-cpp -MMD"
   ;;
esac

case %cmsplatf in
   *_gcc4[3456789]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Werror=type-limits"
   ;;
esac

# Enable visibility inlines hidden. Should drastically remove
# the amount of symbols due to templates.
# FIXME: not enabled on linux, yet, change the case statement
#        to *_gcc4[23456789]* when stable.
case %cmsplatf in
  osx* )
    COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -fvisibility-inlines-hidden"
  ;;
esac

export COMPILER_CXXFLAGS

# Handle here platform specific overrides. In case we
# want to tune something for a specific architecture.
case %cmsplatf in
  osx10[56]*)
     # On macosx we explicitly pick up a compiler version so that there is
     # actually matching between the platform specified to cmsBuild and the
     # compiler.
     export COMPILER_NAME_SUFFIX="-$COMPILER_VERSION_MAJOR.$COMPILER_VERSION_MINOR"
  ;;
esac

# General substitutions
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml

%post
%{relocateConfig}etc/scram.d/*.xml
echo "LLVM_GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv LLVM_GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
