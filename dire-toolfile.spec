### RPM external dire-toolfile 1.0
Requires: dire
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/dire.xml
<tool name="dire" version="@TOOL_VERSION@">
  <lib name="dire"/>
  <client>
    <environment name="DIRE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$DIRE_BASE/lib"/>
    <environment name="INCLUDE" default="$DIRE_BASE/include"/>
  </client>
  <use name="root_cxxdefaults"/>
  <use name="pythia8"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
