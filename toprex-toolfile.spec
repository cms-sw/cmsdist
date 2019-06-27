### RPM external toprex-toolfile 1.0
Requires: toprex
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/toprex.xml
<tool name="toprex" version="@TOOL_VERSION@">
  <lib name="toprex"/>
  <client>
    <environment name="TOPREX_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TOPREX_BASE/lib"/>
  </client>
  <use name="toprex_headers"/>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/toprex_headers.xml
<tool name="toprex_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="TOPREX_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$TOPREX_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE
## IMPORT scram-tools-post

# bla bla
