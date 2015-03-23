### RPM external evtgenlhc-toolfile 1.0
Requires: evtgenlhc
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/evtgenlhc.xml
<tool name="evtgenlhc" version="@TOOL_VERSION@">
  <lib name="evtgenlhc"/>
  <client>
    <environment name="EVTGENLHC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$EVTGENLHC_BASE/lib"/>
    <environment name="INCLUDE" default="$EVTGENLHC_BASE"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="clhep"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

