### RPM cms llvm-gcc-toolfile 13.0

Requires: llvm
BuildRequires: python
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
export LLVM_ROOT
export LLVM_VERSION
export GCC_ROOT
export G77_ROOT

mkdir -p %i/etc/scram.d
# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/llvm-cxxcompiler.xml
  <tool name="llvm-cxxcompiler" version="@LLVM_VERSION@" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="LLVM_CXXCOMPILER_BASE" default="@LLVM_ROOT@"/>
      <environment name="CXX" value="$LLVM_CXXCOMPILER_BASE/bin/clang++"/>
    </client>
    # drop flags not supported by llvm
    # -Wno-non-template-friend removed since it's not supported, yet, by llvm.
    <flags REM_CXXFLAGS="-Wno-non-template-friend"/>
    <flags REM_CXXFLAGS="-Werror=format-contains-nul"/>
    <flags REM_CXXFLAGS="-Werror=maybe-uninitialized"/>
    <flags REM_CXXFLAGS="-Werror=unused-but-set-variable"/>
    <flags REM_CXXFLAGS="-Werror=return-local-addr"/>
    <flags REM_CXXFLAGS="-fipa-pta"/>
    <flags REM_CXXFLAGS="-frounding-math"/>
    <flags REM_CXXFLAGS="-mrecip"/>
    <flags REM_CXXFLAGS="-Wno-psabi"/>
    <flags REM_CXXFLAGS="-fno-crossjumping"/>
    <flags REM_CXXFLAGS="-fno-aggressive-loop-optimizations"/>
    <flags REM_CXXFLAGS="-mlong-double-64"/>
    <flags CXXFLAGS="-Wno-c99-extensions"/>
    <flags CXXFLAGS="-Wno-c++11-narrowing"/>
    <flags CXXFLAGS="-D__STRICT_ANSI__"/>
    <flags CXXFLAGS="-Wno-unused-private-field"/>
    <flags CXXFLAGS="-Wno-unknown-pragmas"/>
    <flags CXXFLAGS="-Wno-unused-command-line-argument"/>
    <flags CXXFLAGS="-Wno-unknown-warning-option"/>
    <flags CXXFLAGS="-ftemplate-depth=512"/>
    <flags CXXFLAGS="-Wno-error=potentially-evaluated-expression"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$LLVM_CXXCOMPILER_BASE/lib64" type="path"/>
    <runtime name="PATH" value="$LLVM_CXXCOMPILER_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/iwyu-cxxcompiler.xml
  <tool name="iwyu-cxxcompiler" version="@LLVM_VERSION@" type="compiler">
    <use name="llvm-cxxcompiler"/>
    <client>
      <environment name="LLVM_CXXCOMPILER_BASE" default="@LLVM_ROOT@"/>
      <environment name="CXX" value="$LLVM_CXXCOMPILER_BASE/bin/include-what-you-use"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/llvm-ccompiler.xml
  <tool name="llvm-ccompiler" version="@LLVM_VERSION@" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="LLVM_CCOMPILER_BASE" default="@LLVM_ROOT@"/>
      <environment name="CC" value="$LLVM_CCOMPILER_BASE/bin/clang"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/llvm-f77compiler.xml
  <tool name="llvm-f77compiler" version="@LLVM_VERSION@" type="compiler">
    <use name="gcc-f77compiler"/>    
    <client>
      <environment name="FC" default="@G77_ROOT@/bin/gfortran"/>
    </client>
  </tool>
EOF_TOOLFILE

#Clang analyzer compilers
cat << \EOF_TOOLFILE >%i/etc/scram.d/llvm-analyzer-cxxcompiler.xml
  <tool name="llvm-analyzer-cxxcompiler" version="@LLVM_VERSION@" type="compiler">
    <use name="llvm-cxxcompiler"/>
    <client>
      <environment name="LLVM_ANALYZER_CXXCOMPILER_BASE" default="@LLVM_ROOT@"/>
      <environment name="CXX" value="$LLVM_ANALYZER_CXXCOMPILER_BASE/bin/c++-analyzer"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/llvm-analyzer-ccompiler.xml
  <tool name="llvm-analyzer-ccompiler" version="@LLVM_VERSION@" type="compiler">
    <use name="llvm-ccompiler"/>
    <client>
      <environment name="LLVM_ANALYZER_CCOMPILER_BASE" default="@LLVM_ROOT@"/>
      <environment name="CC" value="$LLVM_ANALYZER_CCOMPILER_BASE/bin/ccc-analyzer"/>
    </client>
  </tool>
EOF_TOOLFILE

# This is a toolfile to use llvm / clang as a library, not as a compiler.
cat << \EOF_TOOLFILE >%i/etc/scram.d/llvm.xml
  <tool name="llvm" version="@LLVM_VERSION@">
    <lib name="clang"/>
    <client>
      <environment name="LLVM_BASE" default="@LLVM_ROOT@"/>
      <environment name="LIBDIR" default="$LLVM_BASE/lib64"/>
      <environment name="INCLUDE" default="$LLVM_BASE/include"/>
    </client>
    <flags LDFLAGS="-Wl,-undefined -Wl,suppress"/>
    <flags CXXFLAGS="-D_DEBUG -D_GNU_SOURCE -D__STDC_CONSTANT_MACROS"/>
    <flags CXXFLAGS="-D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -O3 "/>
    <flags CXXFLAGS="-fomit-frame-pointer -fPIC -Wno-enum-compare "/>
    <flags CXXFLAGS="-Wno-strict-aliasing -fno-rtti"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/pyclang.xml
<tool name="pyclang" version="@LLVM_VERSION@">
  <client>
    <environment name="PYCLANG_BASE" default="@LLVM_ROOT@"/>
  </client>
  <use name="python"/>
</tool>
EOF_TOOLFILE
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

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
echo "LLVM_GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv LLVM_GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
# bla bla
