### RPM external lcov-toolfile 1.0
Requires: lcov
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/lcov.xml
<tool name="lcov" version="@TOOL_VERSION@">
  <info url="http://ltp.sourceforge.net/coverage/lcov.php"/>
  <client>
    <environment name="LCOV_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$LCOV_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
