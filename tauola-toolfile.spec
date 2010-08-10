### RPM external tauola-toolfile 1.0
Requires: tauola
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tauola.xml
<tool name="tauola" version="@TOOL_VERSION@">
  <lib name="tauola"/>
  <lib name="pretauola"/>
  <client>
    <environment name="TAUOLA_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TAUOLA_BASE/lib"/>
    <environment name="INCLUDE" default="$TAUOLA_BASE/include"/>
  </client>
  <use name="f77compiler"/>
  <use name="pythia6"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
