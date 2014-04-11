### RPM external tauolapp-114-toolfile 1.1.4
Requires: tauolapp-114
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tauolapp.xml
<tool name="tauolapp-144" version="@TOOL_VERSION@">
  <lib name="TauolaCxxInterface_114"/>
  <lib name="TauolaFortran_114"/>
  <lib name="TauolaTauSpinner_114"/>
  <client>
    <environment name="TAUOLAPP_114_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TAUOLAPP_114_BASE/lib"/>
    <environment name="INCLUDE" default="$TAUOLAPP_114_BASE/include"/>
  </client>
  <use name="hepmc"/>
  <use name="f77compiler"/>
  <use name="pythia8"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
