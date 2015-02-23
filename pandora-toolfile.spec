### RPM external pandora-toolfile 1.0
Requires: pandora
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pandora.xml
<tool name="pandora" version="v00-17-CMSp1">
  <info url="http://www.hep.phy.cam.ac.uk/twiki/bin/view/Main/PandoraPFANew"/>
  <lib name="LCContent"/>
  <lib name="PandoraSDK"/>
  <lib name="PandoraMonitoring"/>
   <client>
    <environment name="PANDORA_BASE" default="@TOOL_ROOT@"/>
    <environment name="PANDORA_INTERFACE_BASE" default="@TOOL_ROOT@/include"/>
    <environment name="PANDORA_SDK_INCLUDE"    default="$PANDORA_INTERFACE_BASE/PandoraSDK/include"/>
    <environment name="PANDORA_LCCONTENT_INCLUDE" default="$PANDORA_INTERFACE_BASE/LCContent/include"/>
    <environment name="LIBDIR"             default="$PANDORA_BASE/lib"/>
    <environment name="INCLUDE" value="$PANDORA_SDK_INCLUDE"/>
    <environment name="INCLUDE" value="$PANDORA_LCCONTENT_INCLUDE"/>
   </client>
  <runtime name="LD_LIBRARY_PATH"   value="$PANDORA_BASE/lib"           type="path"/>
  <runtime name="INCLUDE" value="$PANDORA_SDK_INCLUDE" type="path"/>
  <runtime name="INCLUDE" value="$PANDORA_LCCONTENT_INCLUDE" type="path"/>
  <runtime name="PANDORA_SDK_INCLUDE_PATH" value="$PANDORA_SDK_INCLUDE" type="path"/>
  <runtime name="PANDORA_LCCONTENT_INCLUDE_PATH" value="$PANDORA_LCCONTENT_INCLUDE" type="path"/>

</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
