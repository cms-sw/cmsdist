### RPM external xtensor-toolfile 1.0
Requires: xtensor
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/xtensor.xml
<tool name="xtensor" version="@TOOL_VERSION@">
  <info url="https://github.com/QuantStack/xtensor"/>
  <client>
    <environment name="XTENSOR_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$XTENSOR_BASE/include"/>
  </client>
  <use name="xtl"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
