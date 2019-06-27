### RPM external ccache-gcc-toolfile 1.0
Requires: ccache

%prep

%build

%install
export CCACHE_ROOT
export CCACHE_VERSION

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccache-cxxcompiler.xml
  <tool name="ccache-cxxcompiler" version="@CCACHE_VERSION@" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="CXX" value="@CCACHE_ROOT@/bin/c++"/>
      <environment name="BUILDENV_CCACHE_BASEDIR" value="$LOCALTOP" handler="warn"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/ccache-ccompiler.xml
  <tool name="ccache-ccompiler" version="@CCACHE_VERSION@" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="CC" value="@CCACHE_ROOT@/bin/gcc"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/ccache-f77compiler.xml
  <tool name="ccache-f77compiler" version="@CCACHE_VERSION@" type="compiler">
    <use name="gcc-f77compiler"/>
    <client>
      <environment name="FC" default="@CCACHE_ROOT@/bin/gfortran"/>
    </client>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
