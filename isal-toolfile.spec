### RPM external isal-toolfile 1.0
Requires: isal
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/isal.xml
<tool name="isal" version="@TOOL_VERSION@" revision="1">
  <info url="https://github.com/intel/isa-l/wiki"/>
  <lib name="isal"/>
  <client>
    <environment name="ISAL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$ISAL_BASE/lib"/>
    <environment name="INCLUDE" default="$ISAL_BASE/include"/>
  </client>
  <use name="eigen"/>
</tool>
EOF_TOOLFILE
export PYTHON_LIB_SITE_PACKAGES
## IMPORT scram-tools-post
