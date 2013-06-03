### RPM external coin-toolfile 1.0
Requires: coin
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/coin.xml
<tool name="coin" version="@TOOL_VERSION@">
  <info url="http://www.coin3d.org"/>
  <lib name="Coin"/>
  <client>
    <environment name="COIN_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$COIN_BASE/lib"/>
    <environment name="INCLUDE" default="$COIN_BASE/include"/>
  </client>
  <use name="OpenGL"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/openinventor.xml
<tool name="openinventor" version="coin">
  <use name="Coin"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
