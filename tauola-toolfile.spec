### RPM external tauola-toolfile 1.0
Requires: tauola
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tauola.xml
<tool name="tauola" version="@TOOL_VERSION@">
  <lib name="pretauola"/>
  <lib name="tauola"/>
  <client>
    <environment name="TAUOLA_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TAUOLA_BASE/lib"/>
  </client>
  <use name="f77compiler"/>
  <use name="tauola_headers"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tauola_headers.xml
<tool name="tauola_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="TAUOLA_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$TAUOLA_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
