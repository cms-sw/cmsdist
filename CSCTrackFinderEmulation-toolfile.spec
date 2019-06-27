### RPM cms CSCTrackFinderEmulation-toolfile 2.0
Requires: CSCTrackFinderEmulation
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/CSCTrackFinderEmulation.xml
<tool name="CSCTrackFinderEmulation" version="@TOOL_VERSION@">
  <lib name="CSCTrackFinderEmulation"/>
  <client>
    <environment name="CSCTRACKFINDEREMULATION_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CSCTRACKFINDEREMULATION_BASE/lib64"/>
    <environment name="INCLUDE" default="$CSCTRACKFINDEREMULATION_BASE/include"/>
  </client>
  <runtime name="CSC_TRACK_FINDER_DATA_DIR" default="$CSCTRACKFINDEREMULATION_BASE/data/"/>
  <runtime name="CMSSW_SEARCH_PATH" default="$CSCTRACKFINDEREMULATION_BASE/data" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
