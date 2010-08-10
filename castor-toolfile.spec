### RPM external castor-toolfile 1.0
Requires: castor
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/castor.xml
<tool name="castor" version="@TOOL_VERSION@">
  <lib name="shift"/>
  <client>
    <environment name="CASTOR_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$CASTOR_BASE/include"/>
    <environment name="LIBDIR" default="$CASTOR_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
