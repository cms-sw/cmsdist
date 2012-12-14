### RPM cms ccache-gcc-toolfile 1.0
Requires: ccache

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
export CCACHE_GCC_TOOLFILE_ROOT
export CCACHE_GCC_TOOLFILE_VERSION
export GCC_ROOT
export CCACHE_ROOT
export G77_ROOT

mkdir -p %i/etc/scram.d
# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/ccache-cxxcompiler.xml
  <tool name="ccache-cxxcompiler" version="@CCACHE_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="CXX" value="@CCACHE_ROOT@/bin/c++"/>
      <environment name="BUILDENV_CCACHE_BASEDIR" value="$LOCALTOP" handler="warn"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/ccache-ccompiler.xml
  <tool name="ccache-ccompiler" version="@CCACHE_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="CC" value="@CCACHE_ROOT@/bin/gcc"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/ccache-f77compiler.xml
  <tool name="ccache-f77compiler" version="@CCACHE_GCC_TOOLFILE_VERSION@" type="compiler">
    <use name="gcc-f77compiler"/>
    <client>
      <environment name="FC" default="@CCACHE_ROOT@/bin/gfortran"/>
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
