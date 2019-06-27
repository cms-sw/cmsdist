### RPM external coral-toolfile 1.0
Requires: coral
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/coral.xml
<tool name="coral" version="@TOOL_VERSION@" type="scram">
  <client>
    <environment name="CORAL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CORAL_BASE/$SCRAM_ARCH/lib"/>
    <environment name="INCLUDE" default="$CORAL_BASE/include/LCG"/>
  </client>
  <runtime name="PYTHON27PATH" default="$CORAL_BASE/$SCRAM_ARCH/python" type="path"/>
  <runtime name="PYTHON27PATH" default="$CORAL_BASE/$SCRAM_ARCH/lib" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
