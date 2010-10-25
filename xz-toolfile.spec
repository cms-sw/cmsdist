### RPM external xz-toolfile 1.0
Requires: xz

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/xz.xml
  <tool name="xz" version="@TOOL_VERSION@">
    <info url="http://tukaani.org/xz/"/>
    <client>
      <environment name="XZ_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$XZ_BASE/lib"/>
      <environment name="INCLUDE" default="$XZ_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
