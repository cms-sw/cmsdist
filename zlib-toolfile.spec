### RPM external zlib-toolfile 1.0
Requires: zlib
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/zlib.xml
<tool name="zlib" version="@TOOL_VERSION@">
  <lib name="z"/>
  <client>
    <environment name="ZLIB_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$ZLIB_BASE/include"/>
    <environment name="LIBDIR" default="$ZLIB_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
