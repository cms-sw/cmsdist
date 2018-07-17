### RPM external libgit2-toolfile 1.0
Requires: libgit2
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libgit2.xml
<tool name="libgit2" version="@TOOL_VERSION@">
  <info url="http://www.research.att.com/sw/tools/libgit2/"/>
  <lib name="git2"/>
  <client>
    <environment name="LIBGIT2_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBGIT2_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBGIT2_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
