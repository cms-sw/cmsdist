### RPM cms gcc-checker-plugin-toolfile 1.0

# gcc has a separate spec file for the generating a 
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none
Requires: gcc gcc-checker-plugin

%prep
%build
%install
mkdir -p %{i}/etc/scram.d

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-checker-plugin.xml
  <tool name="gcc-checker-plugin" version="@GCC_VERSION@">
    <client>
      <environment name="GCC_CHECKER_PLUGIN_ROOT" default="@GCC_CHECKER_PLUGIN_ROOT@"/>
      <environment name="INCLUDE"   default="$GCC_CHECKER_PLUGIN_ROOT/include"/>
    </client>
  </tool>
  <runtime name="GCC_CHECKER_PLUGIN" default="$GCC_CHECKER_PLUGIN_ROOT/lib/libchecker_gccplugins.so"/>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-analyzer-cxxcompiler.xml
  <tool name="gcc-checker-cxxcompiler" version="@GCC_VERSION@">
    <client>
      <environment name="GCC_CHECKER_PLUGIN_ROOT" default="@GCC_CHECKER_PLUGIN_ROOT@"/>
      <environment name="CXX"   default="@GCC_ROOT@/bin/c++"/>
    </client>
  </tool>
  <flags CXXFLAGS="-fplugin=@GCC_CHECKER_PLUGIN_ROOT@/lib/libchecker_gccplugins.so"/>
  <flags CXXFLAGS="-fplugin-arg-libchecker_gccplugins-checkers=all"/>
  <flags CXXFLAGS="-fsyntax-only"/>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-analyzer-ccompiler.xml
  <tool name="gcc-checker-ccompiler" version="@GCC_VERSION@">
    <client>
      <environment name="GCC_CHECKER_PLUGIN_ROOT" default="@GCC_CHECKER_PLUGIN_ROOT@"/>
      <environment name="CC"   default="@GCC_ROOT@/bin/cc"/>
    </client>
  </tool>
  <flags CFLAGS="-fplugin=@GCC_CHECKER_PLUGIN_ROOT@/lib/libchecker_gccplugins.so"/>
  <flags CFLAGS="-fplugin-arg-libchecker_gccplugins-checkers=all"/>
  <flags CFLAGS="-fsyntax-only"/>
EOF_TOOLFILE

export GCC_CHECKER_PLUGIN_ROOT
export GCC_VERSION
export GCC_ROOT

# General substitutions
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %{i}/etc/scram.d/*.xml

%post
%{relocateConfig}etc/scram.d/*.xml
echo "GCC_CHECKER_PLUGIN_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_CHECKER_PLUGIN_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv GCC_CHECKER_PLUGIN_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
