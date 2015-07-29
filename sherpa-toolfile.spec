### RPM external sherpa-toolfile 1.0
Requires: sherpa
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/sherpa.xml
<tool name="sherpa" version="@TOOL_VERSION@">
<lib name="SherpaMain"/>
<lib name="ToolsMath"/>
<lib name="ToolsOrg"/>
<client>
<environment name="SHERPA_BASE" default="@TOOL_ROOT@"/>
<environment name="BINDIR" default="$SHERPA_BASE/bin"/>
<environment name="LIBDIR" default="$SHERPA_BASE/lib/SHERPA-MC"/>
<environment name="INCLUDE" default="$SHERPA_BASE/include/SHERPA-MC"/>
</client>
<runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$SHERPA_BASE/include" type="path"/>
<runtime name="SHERPA_SHARE_PATH" value="$SHERPA_BASE/share/SHERPA-MC" type="path"/>
<runtime name="SHERPA_INCLUDE_PATH" value="$SHERPA_BASE/include/SHERPA-MC" type="path"/>
<runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
<use name="root_cxxdefaults"/>
<use name="HepMC"/>
<use name="lhapdf"/>
<use name="qd"/>
<use name="blackhat"/>
<use name="fastjet"/>
<use name="sqlite"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
