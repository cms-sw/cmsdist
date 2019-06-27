### RPM external ktjet-toolfile 1.0
Requires: ktjet
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/ktjet.xml
<tool name="ktjet" version="@TOOL_VERSION@">
  <info url="http://hepforge.cedar.ac.uk/ktjet"/>
  <lib name="KtEvent"/>
  <client>
    <environment name="KTJET_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$KTJET_BASE/lib"/>
    <environment name="INCLUDE" default="$KTJET_BASE/include"/>
  </client>
  <flags cppdefines="KTDOUBLEPRECISION"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
