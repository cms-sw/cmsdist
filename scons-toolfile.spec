### RPM external scons-toolfile 1.0
Requires: scons

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/scons.xml
<tool name="scons" version="@TOOL_VERSION@">
  <info url="http://prdownloads.sourceforge.net/scons/"/>
   <lib name="scons"/>
  <client>
    <environment name="SCONS_BASE" default="@TOOL_ROOT@"/>
    <environment name="SCONS_LIB_DIR" default="$SCONS_BASE/lib/scons-1.2.0"/>
    <environment name="BINDIR" default="$SCONS_BASE/bin"/>
  </client>  
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
