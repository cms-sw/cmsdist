### RPM external ittnotify-toolfile 1.0
Requires: ittnotify
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/ittnotify.xml
<tool name="ittnotify" version="@TOOL_VERSION@">
 <lib name="ittnotify"/>
 <client>
    <environment name="ITTNOTIFY_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$ITTNOTIFY_BASE/include"/>
    <environment name="LIBDIR" default="$ITTNOTIFY_BASE/lib"/>
 </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
