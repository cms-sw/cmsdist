### RPM external herwig-toolfile 1.0
Requires: herwig
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/herwig.xml
<tool name="herwig" version="@TOOL_VERSION@">
  <lib name="herwig"/>
  <lib name="herwig_dummy"/>
  <client>
    <environment name="HERWIG_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HERWIG_BASE/lib"/>
    <environment name="INCLUDE" default="$HERWIG_BASE/include"/>
  </client>
  <use name="f77compiler"/>
  <use name="lhapdf"/>
  <use name="tauola"/>
  <use name="photos"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
