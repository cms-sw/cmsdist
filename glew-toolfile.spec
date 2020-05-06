### RPM external glew-toolfile 1.0
Requires: glew
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat <<EOF
 \EOF_TOOLFILE >%i/etc/scram.d/glew.xml
<tool name="glew" version="@TOOL_VERSION@">
  <lib name="GLEW"/>
  <client>
    <environment name="GLEW_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$GLEW_BASE/include"/>
    <environment name="LIBDIR" default="$GLEW_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
