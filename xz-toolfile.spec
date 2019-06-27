### RPM external xz-toolfile 1.1
Requires: xz

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/xz.xml
  <tool name="xz" version="@TOOL_VERSION@">
    <info url="http://tukaani.org/xz/"/>
    <lib name="lzma"/>
    <client>
      <environment name="XZ_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$XZ_BASE/lib"/>
      <environment name="INCLUDE" default="$XZ_BASE/include"/>
    </client>
    <runtime name="PATH" value="$XZ_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
