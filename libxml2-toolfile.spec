### RPM external libxml2-toolfile 1.0
Requires: libxml2
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libxml2.xml
<tool name="libxml2" version="@TOOL_VERSION@">
  <info url="http://xmlsoft.org/"/>
  <lib name="xml2"/>
  <client>
    <environment name="LIBXML2_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBXML2_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBXML2_BASE/include/libxml2"/>
  </client>
  <runtime name="PATH" value="$LIBXML2_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
