### RPM external millepede-toolfile 1.0
Requires: millepede
%prep

%build

%install

mkdir -p %i/etc/scram.d
# millepede tool file
cat << \EOF_TOOLFILE >%i/etc/scram.d/millepede.xml
<tool name="millepede" version="@TOOL_VERSION@">
  <info url="http://www.wiki.terascale.de/index.php/Millepede_II"/>
  <client>
    <environment name="MILLEPEDE_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$MILLEPEDE_BASE/bin" type="path"/>
  <use name="sockets"/>
  <use name="pcre"/>
  <use name="zlib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
