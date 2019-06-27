### RPM external expat-toolfile 1.0
Requires: expat
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/expat.xml
<tool name="expat" version="@TOOL_VERSION@">
  <lib name="expat"/>
  <client>
    <environment name="EXPAT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$EXPAT_BASE/lib"/>
    <environment name="INCLUDE" default="$EXPAT_BASE/include"/>
    <environment name="BINDIR" default="$EXPAT_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$BINDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
