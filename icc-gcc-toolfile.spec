### RPM cms icc-gcc-toolfile 13.0

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif
Source: none

%prep
%build
%install
mkdir -p %i/etc/scram.d

# Determine the GCC_ROOT if "use system compiler is used.  We still need this
# because we need to pick up libstdc++ from the gcc installation since clang
# does not ship its own and because clang does not provide a fortran compiler.
if [ "X$GCC_ROOT" = X ]
then
    GCC_PATH=`which gcc` || exit 1
    GCC_VERSION=`gcc -dumpversion` || exit 1
    GCC_ROOT=`echo $GCC_PATH | sed -e 's|/bin/gcc||'`
    G77_ROOT=$GFORTRAN_MACOSX_ROOT
else
    G77_ROOT=$GCC_ROOT
fi
export ICC_GCC_TOOLFILE_ROOT
export ICC_GCC_TOOLFILE_VERSION
export GCC_ROOT
export G77_ROOT

mkdir -p %i/etc/scram.d
# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/icc-cxxcompiler.xml
  <tool name="icc-cxxcompiler" version="@ICC_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="ICC_CXXCOMPILER_BASE" default="/afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2013"/>
      <environment name="CXX" value="$ICC_CXXCOMPILER_BASE/bin/icpc"/>
    </client>
    # drop flags not supported by llvm
    # -Wno-non-template-friend removed since it's not supported, yet, by llvm.
    <flags REM_CXXFLAGS="-Wno-non-template-friend"/>
    <flags REM_CXXFLAGS="-Werror=format-contains-nul"/>
    <flags REM_CXXFLAGS="-Wno-vla"/>
    <flags REM_CXXFLAGS="-Wstrict-overflow"/>
    <flags REM_CXXFLAGS="-Wno-strict-overflow"/>
    <flags REM_CXXFLAGS="-fipa-pta"/>
    <flags REM_CXXFLAGS="-felide-constructors"/>
    <flags REM_CXXFLAGS="-fdiagnostics-show-option"/>
    <flags REM_CXXFLAGS="-Wno-non-template-friend"/>
    <flags REM_CXXFLAGS="-Werror=format-contains-nul"/>
    <flags REM_CXXFLAGS="-Wunknown-pragmas"/>
    <flags REM_LDFLAGS="-Wl,--icf=all"/>
    <flags CXXFLAGS="-Wno-unknown-pragmas"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$LLVM_CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="PATH" value="$ICC_CXXCOMPILER_BASE/bin" type="path"/>
    <runtime name="COMPILER_RUNTIME_OBJECTS" value="@GCC_ROOT@"/>
    <runtime name="INTEL_LICENSE_FILE" value="28518@lxlic01.cern.ch,28518@lxlic02.cern.ch,28518@lxlic03.cern.ch:/afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2013/composer_xe_2013.0.079/licenses:/opt/intel/licenses:/afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2013/composer_xe_2013.0.079/licenses:/opt/intel/licenses"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/icc-ccompiler.xml
  <tool name="llvm-ccompiler" version="@ICC_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="ICC_CCOMPILER_BASE" default="/afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2013"/>
      <environment name="CC" value="ICC_CCOMPILER_BASE/bin/icc"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/icc-f77compiler.xml
  <tool name="icc-f77compiler" version="@ICC_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-f77compiler"/>    
    <client>
      <environment name="FC" default="@ICC_GCC_TOOLFILE_VERSION@/bin/ifort"/>
    </client>
  </tool>
EOF_TOOLFILE

# NON-empty defaults
# First of all handle OS specific options.
OS_RUNTIME_LDPATH_NAME="LD_LIBRARY_PATH"
case %cmsplatf in
  osx* ) OS_RUNTIME_LDPATH_NAME="DYLD_LIBRARY_PATH" ;;
esac
export OS_RUNTIME_LDPATH_NAME

# General substitutions
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml
%post
%{relocateConfig}etc/scram.d/*.xml
echo "ICC_GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv ICC_GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
