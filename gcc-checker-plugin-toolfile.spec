### RPM cms gcc-checker-plugin-toolfile 1.0
Requires: gcc gcc-checker-plugin

%prep
%build
%install
mkdir -p %{i}/etc/scram.d

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-checker-plugin.xml
  <tool name="gcc-checker-plugin" version="@TOOL_VERSION@">
    <client>
      <environment name="GCC_CHECKER_PLUGIN_ROOT" default="@TOOL_ROOT@"/>
      <environment name="INCLUDE"   default="$GCC_CHECKER_PLUGIN_ROOT/include"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-analyzer-cxxcompiler.xml
  <tool name="gcc-analyzer-cxxcompiler" version="@TOOL_VERSION@" type="compiler">
    <client>
      <environment name="CXX"   default="@GCC_ROOT@/bin/c++"/>
    </client>
  </tool>
  <flags CXXFLAGS="-fplugin=@TOOL_ROOT@/lib/libchecker_gccplugins.so"/>
  <flags CXXFLAGS="-fplugin-arg-libchecker_gccplugins-checkers=all"/>
  <flags CXXFLAGS="-fsyntax-only"/>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-analyzer-ccompiler.xml
  <tool name="gcc-analyzer-ccompiler" version="@TOOL_VERSION@" type="compiler">
    <client>
      <environment name="CC"   default="@GCC_ROOT@/bin/cc"/>
    </client>
  </tool>
  <flags CFLAGS="-fplugin=@TOOL_ROOT@/lib/libchecker_gccplugins.so"/>
  <flags CFLAGS="-fplugin-arg-libchecker_gccplugins-checkers=all"/>
  <flags CFLAGS="-fsyntax-only"/>
EOF_TOOLFILE

export GCC_ROOT

## IMPORT scram-tools-post
# bla bla
