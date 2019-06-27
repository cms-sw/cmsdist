### RPM external catch2-toolfile 1.0
Requires: catch2
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/catch2.xml
<tool name="catch2" version="@TOOL_VERSION@">
  <client>
    <environment name="CATCH2_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$CATCH2_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
