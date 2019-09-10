### RPM external cppcheck-toolfile 1.0
Requires: cppcheck
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cppcheck.xml
<tool name="cppcheck" version="@TOOL_VERSION@">
  <info url="https://github.com/danmar/cppcheck"/>
  <client>
    <environment name="CPPCHECK_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$CPPCHECK_BASE/bin" type="path"/>
  <use name="pcre"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
