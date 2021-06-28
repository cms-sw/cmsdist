### RPM external scons-toolfile 2.0
Requires: py3-scons

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py3-scons.xml
<tool name="py3-scons" version="@TOOL_VERSION@">
  <info url="http://prdownloads.sourceforge.net/scons/"/>
  <client>
    <environment name="PY3_SCONS_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$PY3_SCONS_BASE/bin"/>
  </client>
  <runtime name="PY3_SCONS_LIB_DIR" value="$PY3_SCONS_BASE/lib"/>
  <runtime name="PATH" value="$PY3_SCONS_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
