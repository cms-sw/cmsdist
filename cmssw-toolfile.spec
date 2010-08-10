### RPM external cmssw-toolfile 1.0
Requires: cmssw
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cmssw.xml
<tool name="cmssw" version="@TOOL_VERSION@" type="scram">
  <client>
    <environment name="CMSSW_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CMSSW_BASE/lib/$SCRAM_ARCH"/>
    <environment name="CMSSW_BINDIR" default="$CMSSW_BASE/bin/$SCRAM_ARCH"/>
    <environment name="INCLUDE" default="$CMSSW_BASE/src"/>
    <environment name="INCLUDE" default="$CMSSW_BASE/include/$SCRAM_ARCH"/>
  </client>
  <runtime name="PATH"       value="$CMSSW_BINDIR" type="path"/>
  <runtime name="PYTHONPATH" value="$CMSSW_BINDIR" type="path"/>
  <runtime name="PYTHONPATH" value="$LIBDIR" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
