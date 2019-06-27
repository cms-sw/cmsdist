### RPM external libungif-toolfile 1.0
Requires: libungif
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libungif.xml
<tool name="libungif" version="@TOOL_VERSION@">
  <info url="http://sourceforge.net/projects/libungif"/>
  <lib name="ungif"/>
  <client>
    <environment name="LIBUNGIF_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBUNGIF_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBUNGIF_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
