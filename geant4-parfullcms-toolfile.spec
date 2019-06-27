### RPM external geant4-parfullcms-toolfile 1.0
Requires: geant4-parfullcms

%prep
%build
%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE > %{i}/etc/scram.d/geant4-parfullcms.xml
  <tool name="geant4-parfullcms" version="@TOOL_VERSION@">
    <client>
      <environment name="GEANT4_PARFULLCMS" default="@TOOL_ROOT@"/>
    </client>
    <runtime name="PATH" value="$GEANT4_PARFULLCMS/bin" type="path"/>
    <runtime name="GEANT4_PARFULLCMS_CONFIG_DIR" value="$GEANT4_PARFULLCMS/share/ParFullCMS" type="path"/>
    <runtime name="G4FORCENUMBEROFTHREADS" value="max"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
