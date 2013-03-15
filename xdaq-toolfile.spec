### RPM external xdaq-toolfile 1.0
Requires: xdaq
%prep

%build

%install

case %cmsplatf in
  osx*)
    export XDAQ_OS=macosx
    export XDAQ_PLATFORM=x86
  ;;
  slc*)
    export XDAQ_OS=linux
    export XDAQ_PLATFORM=x86
  ;;
esac

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaq.xml
<tool name="XDAQ" version="@TOOL_VERSION@">
  <info url="http://home.cern.ch/xdaq"/>
  <lib name="toolbox"/>
  <lib name="xdaq"/>
  <lib name="config"/>
  <lib name="xoap"/>
  <lib name="xgi"/>
  <lib name="xdata"/>
  <lib name="cgicc"/>
  <lib name="log4cplus"/>
  <lib name="xcept"/>
  <lib name="logudpappender"/>
  <lib name="peer"/>
  <lib name="logxmlappender"/>
  <lib name="asyncresolv"/>
  <lib name="ptfifo"/>
  <lib name="pthttp"/>
  <lib name="pttcp"/>
  <lib name="i2outils"/>
  <lib name="xdaq2rc"/>
  <lib name="xoapfilter"/>
  <lib name="xalan-c"/>
  <lib name="xalanMsg"/>
  <lib name="wsaddressing"/>
  <lib name="wsclientsubscriber"/>
  <lib name="wseventing"/>
  <lib name="wsserviceeventing"/>
  <client>
    <environment name="XDAQ_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$XDAQ_BASE/lib"/>
    <environment name="BINDIR" default="$XDAQ_BASE/bin"/>
    <environment name="INCLUDE" default="$XDAQ_BASE/include"/>
    <environment name="INCLUDE" default="$XDAQ_BASE/include/@XDAQ_OS@"/>
  </client>
  <flags cppdefines="SOAP__ LITTLE_ENDIAN__"/>
  <flags cppdefines="@XDAQ_OS@"/>
  <runtime name="XDAQ_OS" value="@XDAQ_OS@"/>
  <runtime name="XDAQ_PLATFORM" value="@XDAQ_PLATFORM@"/>
  <runtime name="PATH" value="$BINDIR" type="path"/>
  <runtime name="XDAQ_ROOT" value="$XDAQ_BASE"/>
  <runtime name="XDAQ_DOCUMENT_ROOT" value="$XDAQ_BASE/htdocs"/>
  <use name="xerces-c"/>
  <use name="sockets"/>
  <use name="mimetic"/>
  <use name="libuuid"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaqsentinelutils.xml
<tool name="xdaqsentinelutils" version="@TOOL_VERSION@">
  <info url="http://home.cern.ch/xdaq"/>
  <lib name="sentinelutils"/>
  <use name="xdaq"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaqheader.xml
<tool name="xdaqheader" version="@TOOL_VERSION@">
  <info url="http://home.cern.ch/xdaq"/>
  <client>
    <environment name="XDAQHEADER_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$XDAQHEADER_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
