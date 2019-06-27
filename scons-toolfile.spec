### RPM external scons-toolfile 2.0
Requires: scons

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/scons.xml
<tool name="scons" version="@TOOL_VERSION@">
  <info url="http://prdownloads.sourceforge.net/scons/"/>
  <client>
    <environment name="SCONS_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$SCONS_BASE/bin"/>
  </client>
  <runtime name="SCONS_LIB_DIR" value="$SCONS_BASE/lib"/>
  <runtime name="PATH" value="$SCONS_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
