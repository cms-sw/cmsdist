### RPM external clhep-toolfile 1.0
Requires: clhep
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/clhep.xml
<tool name="clhep" version="@TOOL_VERSION@">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <lib name="CLHEP"/>
  <client>
    <environment name="CLHEP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CLHEP_BASE/lib"/>
    <environment name="INCLUDE" default="$CLHEP_BASE/include"/>
  </client>
  <runtime name="CLHEP_PARAM_PATH" value="$CLHEP_BASE"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$CLHEP_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/clhepheader.xml
<tool name="clhepheader" version="@TOOL_VERSION@">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <client>
    <environment name="CLHEPHEADER_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"    default="$CLHEPHEADER_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
