### RPM external collier-toolfile 1.0
Requires: collier
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/collier.xml
<tool name="collier" version="@TOOL_VERSION@">
  <client>
    <environment name="COLLIER_BASE" default="@TOOL_ROOT@"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

