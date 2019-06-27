### RPM external curl-toolfile 1.0
Requires: curl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/curl.xml
<tool name="curl" version="@TOOL_VERSION@">
  <lib name="curl"/>
  <client>
    <environment name="CURL_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$CURL_BASE/include"/>
    <environment name="LIBDIR"       default="$CURL_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$CURL_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
