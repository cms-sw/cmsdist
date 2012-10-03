### RPM external geners-toolfile 1.0
Requires: geners
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/geners.xml
<tool name="geners" version="@TOOL_VERSION@">
  <lib name="geners"/>
  <client>
    <environment name="GENERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GENERS_BASE/lib"/>
    <environment name="INCLUDE" default="$GENERS_BASE/include"/>
  </client>
  <use name="zlib"/>
  <use name="bz2lib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

