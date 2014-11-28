### RPM cms icc-gcc-toolfile 2.0

Requires: gcc-toolfile
Requires: icc-scram
%define   iccbin_dir  bin/intel64
%define   icclib_dir  compiler/lib/intel64
%define   f77bin_dir  bin/intel64
%define   f77lib_dir  compiler/lib/intel64
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
fi
export ICC_ROOT=$ICC_SCRAM_ROOT
export ICC_VERSION=ICC_SCRAM_VERSION
export GCC_ROOT

mkdir -p %i/etc/scram.d
# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/icc-cxxcompiler.xml
  <tool name="icc-cxxcompiler" version="@ICC_VERSION@" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="ICC_CXXCOMPILER_BASE" default="@ICC_ROOT@/installation" handler="warn"/>
      <environment name="CXX" value="$ICC_CXXCOMPILER_BASE/%{iccbin_dir}/icpc" handler="warn"/>
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
    <flags REM_CXXFLAGS="-ftree-vectorize"/>
    <flags REM_CXXFLAGS="-Wno-unused-local-typedefs"/>
    <flags REM_CXXFLAGS="-msse3"/>
    <flags REM_CXXFLAGS="-Wno-psabi"/>
    <flags REM_LDFLAGS="-Wl,--icf=all"/>
    <flags CXXFLAGS="-Wno-unknown-pragmas"/>
    <flags CXXFLAGS="-axSSE3"/>
    <architecture name="_mic_">
      <flags CXXFLAGS="-mmic"/>
      <flags LDFLAGS="-mmic"/>
    </architecture>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$ICC_CXXCOMPILER_BASE/%{icclib_dir}" type="path" handler="warn"/>
    <runtime name="PATH" value="$ICC_CXXCOMPILER_BASE/%{iccbin_dir}" type="path" handler="warn"/>
    <runtime name="COMPILER_RUNTIME_OBJECTS" value="@GCC_ROOT@" handler="warn"/>
    <runtime name="INTEL_LICENSE_FILE" value="28518@AT@lxlic01.cern.ch,28518@AT@lxlic02.cern.ch,28518@AT@lxlic03.cern.ch" type="path" handler="warn"/>
    <runtime name="INTEL_LICENSE_FILE" value="$ICC_CXXCOMPILER_BASE/licenses" type="path" handler="warn"/>
    <runtime name="INTEL_LICENSE_FILE" value="/opt/intel/licenses" type="path" handler="warn"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/icc-ccompiler.xml
  <tool name="icc-ccompiler" version="@ICC_VERSION@" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="ICC_CCOMPILER_BASE" default="@ICC_ROOT@/installation" handler="warn"/>
      <environment name="CC" value="$ICC_CCOMPILER_BASE/%{iccbin_dir}/icc" handler="warn"/>
    </client>
    <architecture name="_mic_">
      <flags CFLAGS="-mmic"/>
    </architecture>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/icc-f77compiler.xml
  <tool name="icc-f77compiler" version="@ICC_VERSION@" type="compiler">
    <use name="gcc-f77compiler"/>    
    <client>
      <environment name="ICC_FCOMPILER_BASE" default="@ICC_ROOT@/ifort" handler="warn"/>
      <environment name="FC" default="$ICC_FCOMPILER_BASE/%{f77bin_dir}/ifort" handler="warn"/>
      <environment name="LIBDIR" default="$ICC_FCOMPILER_BASE/%{f77lib_dir}" handler="warn"/>
    </client>
    <architecture name="_mic_">
      <flags FFLAGS="-mmic"/>
    </architecture>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$ICC_FCOMPILER_BASE/%{f77lib_dir}" type="path" handler="warn"/>
    <lib name="ifcore"/>
    <lib name="ifport"/>
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
export AT="@"
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml
%post
%{relocateConfig}etc/scram.d/*.xml
echo "ICC_GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export ICC_GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv ICC_GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
