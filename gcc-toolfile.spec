### RPM cms gcc-toolfile 11.0

# gcc has a separate spec file for the generating a
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%build
%install
mkdir -p %i/etc/scram.d

# Determine the GCC_ROOT if "use system compiler is used.
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
    <flags CXXFLAGS="-O2 -pedantic -ansi -pthread -pipe"/>
    <flags CXXFLAGS="@ARCH_CXXFLAGS@ @COMPILER_CXXFLAGS@"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses -Wno-deprecated -Werror=return-type -Werror=missing-braces -Werror=unused-value -Werror=address -Werror=format -Werror=sign-compare -Werror=write-strings -Werror=strict-overflow -fdiagnostics-show-option"/>
    <flags LDFLAGS="@OS_LDFLAGS@"/>
    <flags CXXSHAREDFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@"/>
    <flags SHAREDSUFFIX="@OS_SHAREDSUFFIX@"/>
    <flags SCRAM_LANGUAGE_TYPE="C++"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$GCC_BASE/@OS_LIB64DIR@" type="path"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$GCC_BASE/lib" type="path"/>
    <runtime name="PATH" value="$GCC_BASE/bin" type="path"/>
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

cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler.xml
  <tool name="f77compiler" version="@GCC_VERSION@" type="compiler">
    <lib name="gfortran"/>
    <lib name="m"/>
    <client>
      <environment name="F77COMPILER_BASE" default="@G77_ROOT@"/>
      <environment name="FC" default="$F77COMPILER_BASE/bin/gfortran"/>
    </client>
    <flags SCRAM_COMPILER_NAME="gcc@COMPILER_VERSION@"/>
    <flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2"/>
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
    export OS_SHAREDFLAGS="-Wl,-E"
    export OS_SHAREDSUFFIX="so"
    export OS_LIB64DIR="lib64"
    export OS_LDFLAGS="-Wl,-E -Wl,--hash-style=gnu"
    export OS_RUNTIME_LDPATH_NAME="LD_LIBRARY_PATH"
  ;;
  osx* )
    export OS_SHAREDFLAGS="-shared -dynamic -single_module"
    export OS_SHAREDSUFFIX="dylib"
    export OS_LIB64DIR="lib"
    export OS_RUNTIME_LDPATH_NAME="DYLD_LIBRARY_PATH"
  ;;
esac

# Then handle OS + architecture specific options (maybe we should enable more
# aggressive optimizations for amd64 as well??)
case %cmsplatf in
  osx*_ia32_* )
    export ARCH_CXXFLAGS="-arch i386"
    export ARCH_SHAREDFLAGS="-arch i386"
  ;;
  osx*_amd64_* )
    export ARCH_CXXFLAGS="-arch x86_64"
    export ARCH_SHAREDFLAGS="-arch x86_64"
  ;;
  osx*_ppc32_* )
    export ARCH_CXXFLAGS="-arch ppc"
    export ARCH_SHAREDFLAGS="-arch ppc"
  ;;
  slc* )
    # For some reason on mac, some of the header do not compile if this is
    # defined.  Ignore for now.
    export ARCH_CXXFLAGS="-Werror=overflow"
  ;;
esac

# Then handle compiler specific options. E.g. enable
# optimizations as they become available in gcc.
case %cmsplatf in
   *_gcc4[56789]* )
     export COMPILER_CXXFLAGS="-ftree-vectorize"
   ;;
esac

case %cmsplatf in
   *_gcc4[3456789]* )
     export COMPILER_CXXFLAGS="-Werror=array-bounds -Werror=format-contains-nul"
   ;;
esac

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
[ "X$RPM_INSTALL_PREFIX" == "X$CMS_INSTALL_PREFIX" ] || perl -p -i -e "s|$RPM_INSTALL_PREFIX|$CMS_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/%{pkgrel}/etc/scram.d/*.xml
echo "GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
