### RPM external qd-toolfile 1.0
Requires: qd

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/qd.xml
<tool name="qd" version="@TOOL_VERSION@">
  <lib name="qdmod"/>
  <lib name="qd"/>
  <client>
    <environment name="QD_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$QD_BASE/lib"/>
    <environment name="INCLUDE" default="$QD_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qd_f_main.xml
<tool name="qd_f_main" version="@TOOL_VERSION@">
  <lib name="qd_f_main"/>
  <use name="qd"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post


# bla bla
