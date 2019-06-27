### RPM external lz4-toolfile 1.0
Requires: lz4

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/lz4.xml
  <tool name="lz4" version="@TOOL_VERSION@">
    <info url="https://github.com/lz4/lz4"/>
    <lib name="lz4"/>
    <client>
      <environment name="LZ4_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$LZ4_BASE/lib"/>
      <environment name="INCLUDE" default="$LZ4_BASE/include"/>
    </client>
    <runtime name="PATH" value="$LZ4_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
