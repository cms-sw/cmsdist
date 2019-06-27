### RPM external libhepml-toolfile 1.0
Requires: libhepml
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libhepml.xml
<tool name="libhepml" version="@TOOL_VERSION@">
  <lib name="hepml"/>
  <client>
    <environment name="LIBHEPML_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBHEPML_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBHEPML_BASE/interface"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
