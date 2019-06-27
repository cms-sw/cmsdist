### RPM external bz2lib-toolfile 1.0
Requires: bz2lib
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/bz2lib.xml
<tool name="bz2lib" version="@TOOL_VERSION@">
  <info url="http://sources.redhat.com/bzip2/"/>
  <lib name="bz2"/>
  <client>
    <environment name="BZ2LIB_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"       default="$BZ2LIB_BASE/lib"/>
    <environment name="INCLUDE"      default="$BZ2LIB_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
