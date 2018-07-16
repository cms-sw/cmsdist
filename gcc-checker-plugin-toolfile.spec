### RPM cms gcc-checker-plugin-toolfile 1.0

# gcc has a separate spec file for the generating a 
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none
Requires: gcc-checker-plugin

%prep
%build
%install
mkdir -p %{i}/etc/scram.d

# Determine the GCC_ROOT if "use system compiler" is used.
if [ "X$GCC_ROOT" = X ]
then
    export GCC_PATH=$(which gcc) || exit 1
    export GCC_ROOT=$(echo $GCC_PATH | sed -e 's|/bin/gcc||')
    export GCC_VERSION=$(gcc -dumpversion) || exit 1
    export G77_ROOT=$GCC_ROOT
else
    export GCC_PATH
    export GCC_ROOT
    export GCC_VERSION
    export G77_ROOT=$GCC_ROOT
fi
# GCC tool file for explicity linking gcc plugin library
cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-checker-plugin.xml
  <tool name="gcc-checker-plugin" version="@GCC_VERSION@">
    <lib name="checker_gccplugins"/>
    <client>
      <environment name="GCC_CHECKER_PLUGIN_ROOT" default="@GCC_CHECKER_PLUGIN_ROOT@"/>
      <environment name="LIBRARY"   default="$GCC_CHECKER_PLUGIN_ROOT/lib"/>
    </client>
  </tool>
  <runtime name="GCC_CHECKER_PLUGIN" default="$GCC_CHECKER_PLUGIN_ROOT/lib/libchecker_gccplugins.so"/>
EOF_TOOLFILE
export GCC_CHECKER_PLUGIN_ROOT

# General substitutions
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %{i}/etc/scram.d/*.xml

%post
%{relocateConfig}etc/scram.d/*.xml
echo "GCC_CHECKER_PLUGIN_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_CHECKER_PLUGIN_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv GCC_CHECKER_PLUGIN_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
