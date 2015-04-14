### RPM external file-toolfile 1.0
Requires: file

%prep
%build
%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE > %{i}/etc/scram.d/file.xml
  <tool name="file" version="@TOOL_VERSION@">
    <lib name="magic"/>
    <client>
      <environment name="FILE_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$FILE_BASE/lib"/>
      <environment name="INCLUDE" default="$FILE_BASE/include"/>
    </client>
    <runtime name="PATH" value="$FILE_BASE/bin" type="path"/>
    <runtime name="MAGIC" value="$FILE_BASE/share/misc/magic.mgc"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
