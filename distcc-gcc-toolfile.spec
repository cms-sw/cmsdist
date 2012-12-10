### RPM cms distcc-gcc-toolfile 1.0
Requires: distcc

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
export DISTCC_GCC_TOOLFILE_ROOT
export DISTCC_GCC_TOOLFILE_VERSION
export GCC_ROOT
export DISTCC_ROOT
export G77_ROOT

mkdir -p %i/etc/scram.d
# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/distcc-cxxcompiler.xml
  <tool name="distcc-cxxcompiler" version="@DISTCC_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="CXX" value="@DISTCC_ROOT@/bin/c++"/>
    </client>
    # drop flags not supported by llvm
    # -Wno-non-template-friend removed since it's not supported, yet, by llvm.
    <runtime name="PATH" value="$DISTCC_CXXCOMPILER_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/distcc-ccompiler.xml
  <tool name="distcc-ccompiler" version="@DISTCC_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="CC" value="@DISTCC_ROOT@/bin/gcc"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/distcc-f77compiler.xml
  <tool name="distcc-f77compiler" version="@DISTCC_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-f77compiler"/>
    <client>
      <environment name="FC" default="@DISTCC_ROOT@/bin/gfortran"/>
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
export AT="@"
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml
%post
%{relocateConfig}etc/scram.d/*.xml
echo "ICC_GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv ICC_GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
