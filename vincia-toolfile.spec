### RPM external vincia-toolfile 2.0
Requires: vincia
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/vincia.xml
<tool name="vincia" version="@TOOL_VERSION@">
  <lib name="vincia"/>
  <client>
    <environment name="VINCIA_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$VINCIA_BASE/lib"/>
    <environment name="INCLUDE" default="$VINCIA_BASE/include"/>
  </client>
  <runtime name="VINCIADATA" value="$VINCIA_BASE/share/Vincia/xmldoc"/>
  <use name="root_cxxdefaults"/>
  <use name="pythia8"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
