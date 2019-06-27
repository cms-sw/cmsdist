### RPM external charybdis-toolfile 1.0
Requires: charybdis
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/charybdis.xml
<tool name="charybdis" version="@TOOL_VERSION@">
  <info url="http://www.ippp.dur.ac.uk/montecarlo/leshouches/generators/charybdis/"/>
  <lib name="charybdis"/>
  <client>
    <environment name="CHARYBDIS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CHARYBDIS_BASE/lib"/>
    <environment name="INCLUDE" default="$CHARYBDIS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="f77compiler"/>
  <use name="herwig"/>
  <use name="pythia6"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
