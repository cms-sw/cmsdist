### RPM external xtl-toolfile 1.0
Requires: xtl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/xtl.xml
<tool name="xtl" version="@TOOL_VERSION@">
  <info url="https://github.com/QuantStack/xtl"/>
  <client>
    <environment name="XTL_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$XTL_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
