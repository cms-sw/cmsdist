### RPM lcg rootcint-mic-toolfile 1.0
Requires: rootcint-mic
%prep

%build

%install

mkdir -p %i/etc/scram.d
# root_interface toolfile
# rootcint-mic toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/%{n}.xml
<tool name="%{n}" version="@TOOL_VERSION@">
  <client>
    <environment name="ROOTCINT_MIC_BASE" default="@TOOL_ROOT@"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
