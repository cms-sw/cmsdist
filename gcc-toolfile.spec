### RPM cms gcc-toolfile 12.0

# gcc has a separate spec file for the generating a 
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%build
%install
mkdir -p %i/etc/scram.d

# Determine the GCC_ROOT if "use system compiler" is used.
if [ "X$GCC_ROOT" = X ]
then
    export GCC_PATH=`which gcc` || exit 1
    export GCC_ROOT=`echo $GCC_PATH | sed -e 's|/bin/gcc||'`
    export GCC_VERSION=`gcc -dumpversion` || exit 1
    export G77_ROOT=$GCC_ROOT
else
    export GCC_PATH
    export GCC_ROOT
    export GCC_VERSION
    export G77_ROOT=$GCC_ROOT
fi

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

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-cxxcompiler.xml
  <tool name="gcc-cxxcompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_CXXCOMPILER_BASE" default="@GCC_ROOT@"/>
      <environment name="CXX" value="$GCC_CXXCOMPILER_BASE/bin/c++@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags CPPDEFINES="GNU_GCC _GNU_SOURCE @OS_CPPDEFINES@ @ARCH_CPPDEFINES@ @COMPILER_CPPDEFINES@"/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC @OS_CXXSHAREDOBJECTFLAGS@ @ARCH_CXXSHAREDOBJECTFLAGS@ @COMPILER_CXXSHAREDOBJECTFLAGS@"/>
    <flags CXXFLAGS="-O2 -pthread -pipe -Werror=main -Werror=pointer-arith"/>
    <flags CXXFLAGS="-Werror=overlength-strings -Wno-vla @OS_CXXFLAGS@ @ARCH_CXXFLAGS@ @COMPILER_CXXFLAGS@"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wreturn-type"/>
    <flags CXXFLAGS="-Wunused -Wparentheses -Wno-deprecated -Werror=return-type"/>
    <flags CXXFLAGS="-Werror=missing-braces -Werror=unused-value"/>
    <flags CXXFLAGS="-Werror=address -Werror=format -Werror=sign-compare"/>
    <flags CXXFLAGS="-Werror=write-strings -Werror=delete-non-virtual-dtor"/>
    <flags CXXFLAGS="-Werror=maybe-uninitialized -Werror=strict-aliasing"/>
    <flags CXXFLAGS="-Werror=narrowing -Werror=uninitialized"/>
    <flags CXXFLAGS="-Werror=unused-but-set-variable -Werror=reorder"/>
    <flags CXXFLAGS="-Werror=unused-variable -Werror=conversion-null"/>
    <flags CXXFLAGS="-Werror=return-local-addr"/>
    <flags CXXFLAGS="-Werror=switch -fdiagnostics-show-option"/>
    <flags CXXFLAGS="-Wno-unused-local-typedefs -Wno-attributes -Wno-psabi"/>
    <flags LDFLAGS="@OS_LDFLAGS@ @ARCH_LDFLAGS@ @COMPILER_LDFLAGS@"/>
    <flags CXXSHAREDFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@ @COMPILER_SHAREDFLAGS@"/>
    <flags LD_UNIT="@OS_LD_UNIT@ @ARCH_LD_UNIT@ @COMPILER_LD_UNIT@"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$GCC_CXXCOMPILER_BASE/@ARCH_LIB64DIR@" type="path"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$GCC_CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="PATH" value="$GCC_CXXCOMPILER_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-ccompiler.xml
  <tool name="gcc-ccompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_CCOMPILER_BASE" default="@GCC_ROOT@"/>
      <environment name="CC" value="$GCC_CCOMPILER_BASE/bin/gcc@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags CSHAREDOBJECTFLAGS="-fPIC @OS_CSHAREDOBJECTFLAGS@ @ARCH_CSHAREDOBJECTFLAGS@ @COMPILER_CSHAREDOBJECTFLAGS@"/>
    <flags CFLAGS="-O2 -pthread @OS_CFLAGS@ @ARCH_CFLAGS@ @COMPILER_CFLAGS@"/>
  </tool>
EOF_TOOLFILE

# Notice that on OSX we have a LIBDIR defined for f77compiler because gcc C++
# compiler (which comes from the system) does not know about where to find
# libgfortran. 
cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-f77compiler.xml
  <tool name="gcc-f77compiler" version="@GCC_VERSION@" type="compiler">
    <lib name="gfortran"/>
    <lib name="m"/>
    <client>
      <environment name="GCC_F77COMPILER_BASE" default="@G77_ROOT@"/>
      <environment name="FC" default="$GCC_F77COMPILER_BASE/bin/gfortran"/>
      @ARCH_FORTRAN_LIBDIR@
    </client>
    <flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2 @OS_FFLAGS@ @ARCH_FFLAGS@ @COMPILER_FFLAGS@"/>
    <flags FOPTIMISEDFLAGS="-O2 @OS_FOPTIMISEDFLAGS@ @ARCH_FOPTIMISEDFLAGS@ @COMPILER_FOPTIMISEDFLAGS@"/>
    <flags FSHAREDOBJECTFLAGS="-fPIC @OS_FSHAREDOBJECTFLAGS@ @ARCH_FSHAREDOBJECTFLAGS@ @COMPILER_FSHAREDOBJECTFLAGS@"/>
  </tool>
EOF_TOOLFILE

# NON-empty defaults
# First of all handle OS specific options.
%if %islinux
  export OS_SHAREDFLAGS="-shared -Wl,-E"
  export OS_LDFLAGS="-Wl,-E -Wl,--hash-style=gnu"
  export OS_RUNTIME_LDPATH_NAME="LD_LIBRARY_PATH"
  export OS_CXXFLAGS="-Werror=overflow"
%endif
%if %isdarwin
  export OS_SHAREDFLAGS="-shared -dynamic -single_module"
  export OS_LDFLAGS="-Wl,-commons -Wl,use_dylibs"
  export OS_RUNTIME_LDPATH_NAME="DYLD_LIBRARY_PATH"
%endif

# Then handle OS + architecture specific options (maybe we should enable more
# aggressive optimizations for amd64 as well??)
case %cmsplatf in
  osx*)
    export ARCH_CXXFLAGS="-arch x86_64"
    export ARCH_SHAREDFLAGS="-arch x86_64"
    export ARCH_LIB64DIR="lib"
    export ARCH_LD_UNIT="-r"
  ;;
  slc*)
    # For some reason on mac, some of the header do not compile if this is
    # defined.  Ignore for now.
    export ARCH_LIB64DIR="lib64"
    export ARCH_LD_UNIT="-r -m elf_x86_64 -z muldefs"
  ;;
  *_armv7hl_*)
    export ARCH_LIB64DIR="lib"
    export ARCH_LD_UNIT="-r -z muldefs"
  ;;
  *) 
    echo "Unsupported."
    exit 1
  ;;
esac

# Then handle compiler specific options. E.g. enable
# optimizations as they become available in gcc.
COMPILER_CXXFLAGS=

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
   *_amd64_gcc4[56789]* )
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -std=c++11 -msse3 -ftree-vectorize -Wno-strict-overflow"
   ;;
   *_armv7hl_* )
    COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -std=c++11 -ftree-vectorize -Wno-strict-overflow -fsigned-char -fsigned-bitfields"
   ;;
esac

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

# More customizations when using gcc 4.7.x
# See: https://hypernews.cern.ch/HyperNews/CMS/get/edmFramework/2955.html
case %cmsplatf in
  *_gcc4[789]*)
    COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -fno-math-errno --param vect-max-version-for-alias-checks=50 -fipa-pta"
  ;;
esac

# Compressed debug sections for linker
case %cmsplatf in
  *_gcc49*)
    COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Wa,--compress-debug-sections"
  ;;
esac

export COMPILER_CXXFLAGS

# General substitutions
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml

%post
%{relocateConfig}etc/scram.d/*.xml
echo "GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
