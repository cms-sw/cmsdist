### RPM cms gcc-toolfile 11.0

# gcc has a separate spec file for the generating a 
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none

%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%build
%install
mkdir -p %i/etc/scram.d

# Determine the GCC_ROOT if "use system compiler" is used.
if [ "X$GCC_ROOT" = X ]
then
    export GCC_PATH=`which gcc` || exit 1
    export GCC_ROOT=`echo $GCC_PATH | sed -e 's|/bin/gcc||'`
    export GCC_VERSION=`gcc -v 2>&1 | grep "gcc version" | sed 's|[^0-9]*\([0-9].[0-9].[0-9]\).*|\1|'` || exit 1
    export G77_ROOT=$GCC_ROOT
else
    export GCC_PATH
    export GCC_ROOT
    export GCC_VERSION
    export G77_ROOT=$GCC_ROOT
fi

case %cmsplatf in
  osx*_*_gcc421)
    # on Mac OS X, override G77_ROOT with GFORTRAN_MACOSX_ROOT
    export G77_ROOT=$GFORTRAN_MACOSX_ROOT
  ;;
  osx*)
    export G77_ROOT=$GCC_ROOT 
  ;;
esac

case %cmsplatf in
  slc*_*_gcc4[012345]*) ;;
  *) export ARCH_FFLAGS="-cpp" ;;
esac

export COMPILER_VERSION=`echo %cmsplatf | sed -e 's|.*gcc\([0-9]*\).*|\1|'`
export COMPILER_VERSION_MAJOR=`echo %cmsplatf | sed -e 's|.*gcc\([0-9]\).*|\1|'`
export COMPILER_VERSION_MINOR=`echo %cmsplatf | sed -e 's|.*gcc[0-9]\([0-9]\).*|\1|'`

# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler.xml
  <tool name="cxxcompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="CXXCOMPILER_BASE" default="@GCC_ROOT@"/>
      <environment name="GCCBINDIR" default="$CXXCOMPILER_BASE/bin"/>
      <environment name="CXX" value="$GCCBINDIR/c++@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags SCRAM_COMPILER_NAME="gcc@COMPILER_VERSION@"/>
    <flags CCCOMPILER="gcc@COMPILER_VERSION_MAJOR@"/>
    <flags MODULEFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@"/>
    <flags CXXDEBUGFLAG="-g"/>
    <flags CPPDEFINES="GNU_GCC"/>
    <flags CPPDEFINES="_GNU_SOURCE"/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC"/>
    <flags CXXFLAGS="-O2 -pedantic -ansi -pthread -pipe -Wno-vla"/>
    <flags CXXFLAGS="@ARCH_CXXFLAGS@ @COMPILER_CXXFLAGS@"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wreturn-type -Wunused -Wparentheses -Wno-deprecated -Werror=return-type -Werror=missing-braces -Werror=unused-value -Werror=address -Werror=format -Werror=sign-compare -Werror=write-strings -fdiagnostics-show-option"/>
    <flags LDFLAGS="@OS_LDFLAGS@"/>
    <flags CXXSHAREDFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@"/>
    <flags SHAREDSUFFIX="@OS_SHAREDSUFFIX@"/>
    <flags LD_UNIT="@OS_LD_UNIT@ @ARCH_LD_UNIT@"/>
    <flags SCRAM_LANGUAGE_TYPE="C++"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$CXXCOMPILER_BASE/@ARCH_LIB64DIR@" type="path"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="PATH" value="$CXXCOMPILER_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler.xml
  <tool name="ccompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="CCOMPILER_BASE" default="@GCC_ROOT@"/>
      <environment name="GCCBINDIR" value="$CCOMPILER_BASE/bin"/>
      <environment name="CC" value="$GCCBINDIR/gcc@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags CDEBUGFLAG="-g"/>
    <flags CSHAREDOBJECTFLAGS="-fPIC"/>
    <flags CFLAGS="-pthread"/>
    <flags CFLAGS="-O2"/>
    <flags LDFLAGS="@OS_LDFLAGS@"/>
    <flags CSHAREDFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@"/>
    <flags SCRAM_COMPILER_NAME="gcc@COMPILER_VERSION@"/>
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
    <flags SCRAM_COMPILER_NAME="gcc@COMPILER_VERSION@"/>
    <flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2 @ARCH_FFLAGS@"/>
    <flags FCO2FLAG="-O2"/>
    <flags FCOPTIMISED="-O2"/>
    <flags FCDEBUGFLAG="-g"/>
    <flags FCSHAREDOBJECTFLAGS="-fPIC"/>
    <flags SCRAM_LANGUAGE_TYPE="FORTRAN"/>
  </tool>
EOF_TOOLFILE

# NON-empty defaults
export COMPILER_EXEC_NAME="c++"

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
  osx*_amd64_gcc421 )
    export ARCH_CXXFLAGS="-arch x86_64"
    export ARCH_SHAREDFLAGS="-arch x86_64"
    export ARCH_LIB64DIR="lib"
    export ARCH_FORTRAN_LIBDIR='<environment name="LIBDIR" default="$F77COMPILER_BASE/lib/gcc/i686-apple-darwin10/4.2.1/x86_64"/>'
  ;;
  osx*)
    export ARCH_CXXFLAGS="-arch x86_64"
    export ARCH_SHAREDFLAGS="-arch x86_64"
    export ARCH_LIB64DIR="lib"
  ;;
  slc*)
    # For some reason on mac, some of the header do not compile if this is
    # defined.  Ignore for now.
    export ARCH_CXXFLAGS="-Werror=overflow"
    export ARCH_LIB64DIR="lib64"
    export ARCH_LD_UNIT="-r -m elf_x86_64"
  ;;
  *) 
    echo "Unsupported."
    exit 1
  ;;
esac

# Then handle compiler specific options. E.g. enable
# optimizations as they become available in gcc.
COMPILER_CXXFLAGS=
# The following is the default even if not set here
F77_MMD="-MMD"

# Set the following for all gcc < 4.6. gcc46 claims it is no longer needed
# This is perhaps the case also for the earlier versions, but leave it
# there for now.
case %cmsplatf in
   *_gcc4[2345]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Wimplicit"
   ;;
esac

# The following causes problems for gcc46 and boost 1.45.0 so downgrade it
case %cmsplatf in
   *_gcc4[2345]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Werror=strict-overflow"
   ;;
   *_gcc4[6789]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Wstrict-overflow"
   ;;
esac


case %cmsplatf in
   *_gcc4[56789]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -std=c++0x -msse3 -ftree-vectorize -Wno-strict-overflow"
     F77_MMD="-cpp -MMD"
   ;;
esac
export F77_MMD

case %cmsplatf in
   *_gcc4[3456789]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits"
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
  *_gcc4[56789]* )
    COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -fvisibility-inlines-hidden"
  ;;
esac

export COMPILER_CXXFLAGS

# Handle here platform specific overrides. In case we
# want to tune something for a specific architecture.
case %cmsplatf in
  osx*_*_gcc421)
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
echo "GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
