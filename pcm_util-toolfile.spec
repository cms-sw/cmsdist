### RPM external pcm_util-toolfile 1.0
Requires: pcm_util
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pcm_util.xml
<tool name="pcm_util" version="@TOOL_VERSION@">
  <client>
    <environment name="PCM_UTIL_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PCM_UTIL_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

