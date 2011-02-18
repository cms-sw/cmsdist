### RPM cms online-toolfile 2.0
Requires: online
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/online.xml
<tool name="cmssw" version="@TOOL_VERSION@" type="scram">
  <client>
    <environment name="CMSSW_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CMSSW_BASE/lib/$SCRAM_ARCH"/>
    <environment name="CMSSW_BINDIR" default="$CMSSW_BASE/bin/$SCRAM_ARCH"/>
    <environment name="INCLUDE" default="$CMSSW_BASE/src"/>
  </client>
  <runtime name="LD_LIBRARY_PATH" value="$CMSSW_BASE/lib/$SCRAM_ARCH" type="path"/>
  <runtime name="PATH"       value="$CMSSW_BINDIR" type="path"/>
  <runtime name="PYTHONPATH" value="$CMSSW_BINDIR" type="path"/>
  <runtime name="PYTHONPATH" value="$LIBDIR" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
