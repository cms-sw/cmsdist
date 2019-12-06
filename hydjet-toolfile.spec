### RPM external hydjet-toolfile 1.0
Requires: hydjet
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/hydjet.xml
<tool name="hydjet" version="@TOOL_VERSION@">
  <lib name="hydjet"/>
  <client>
    <environment name="HYDJET_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HYDJET_BASE/lib"/>
  </client>
  <use name="pyquen"/>
  <use name="pythia6"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
