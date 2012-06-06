### RPM external nspr-toolfile 1.0
Requires: nspr
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/nspr.xml
  <tool name="nspr" version="@TOOL_VERSION@">
    <lib name="nspr4"/>
    <lib name="plc4"/>
    <lib name="plds4"/>
    <client>
      <environment name="NSPR_BASE" default="@TOOL_ROOT@"/>
      <environment name="INCLUDE" default="$NSPR_BASE/include"/>
      <environment name="LIBDIR" default="$NSPR_BASE/lib"/>
    </client>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
