### RPM external codechecker-toolfile 1.0
Requires: codechecker
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/codechecker.xml
<tool name="codechecker" version="@TOOL_VERSION@">
  <runtime name="PATH" value="@TOOL_ROOT@/bin" type="path"/>
</tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
