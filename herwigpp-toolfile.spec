### RPM external herwigpp-toolfile 1.0
Requires: herwigpp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/herwigpp.xml
<tool name="herwigpp" version="@TOOL_VERSION@">
  <lib name="HerwigAPI"/>
  <client>
    <environment name="HERWIGPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HERWIGPP_BASE/lib/Herwig"/>
    <environment name="INCLUDE" default="$HERWIGPP_BASE/include"/>
    <environment name="BINDIR" default="$HERWIGPP_BASE/bin"/>
  </client>
  <runtime name="HERWIGPATH" value="$HERWIGPP_BASE/share/Herwig"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="PATH" default="$BINDIR" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="lhapdf"/>
  <use name="thepeg"/>
  <use name="madgraph5amcatnlo"/>
%ifnarch ppc64le
  <use name="openloops"/>
%endif
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

