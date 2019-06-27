### RPM external evtgen-toolfile 1.0
Requires: evtgen

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/evtgen.xml
<tool name="evtgen" version="@TOOL_VERSION@">
  <lib name="EvtGen"/>
  <lib name="EvtGenExternal"/>
  <client>
    <environment name="EVTGEN_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$EVTGEN_BASE/lib"/>
    <environment name="INCLUDE" default="$EVTGEN_BASE/include"/>
  </client>
  <runtime name="EVTGENDATA" value="$EVTGEN_BASE/share"/>
  <use name="hepmc"/>
  <use name="pythia8"/>
  <use name="tauolapp"/>
  <use name="photospp"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
