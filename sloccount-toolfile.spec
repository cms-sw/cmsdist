### RPM external sloccount-toolfile 1.0
Requires: sloccount

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/sloccount.xml
  <tool name="sloccount" version="@TOOL_VERSION@">
    <info url="http://www.dwheeler.com/sloccount/"/>
    <client>
      <environment name="SLOCCOUNT_BASE" default="@TOOL_ROOT@"/>
    </client>
    <runtime name="PATH" value="$SLOCCOUNT_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
