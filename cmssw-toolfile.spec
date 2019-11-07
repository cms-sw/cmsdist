### RPM cms cmssw-toolfile CMSSW_9_3_16
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
  </client>
  <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$CMSSW_BASE/biglib/$SCRAM_ARCH" type="path"/>
  <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$CMSSW_BASE/lib/$SCRAM_ARCH" type="path"/>
  <runtime name="PATH"       value="$CMSSW_BINDIR" type="path"/>
  <runtime name="PYTHONPATH" value="$CMSSW_BINDIR" type="path"/>
  <runtime name="PYTHONPATH" value="$LIBDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="CMSSW_FULL_RELEASE_BASE" value="$CMSSW_BASE"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

export OS_RUNTIME_LDPATH_NAME="LD_LIBRARY_PATH"
case %cmsplatf in
  osx* )
    export OS_RUNTIME_LDPATH_NAME="DYLD_FALLBACK_LIBRARY_PATH"
  ;;
esac

## IMPORT scram-tools-post
