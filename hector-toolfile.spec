### RPM external hector-toolfile 1.0
Requires: hector
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/hector.xml
<tool name="Hector" version="@TOOL_VERSION@">
  <info url="http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/"/>
  <lib name="Hector"/>
  <client>
    <environment name="HECTOR_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HECTOR_BASE/lib"/>
    <environment name="INCLUDE" default="$HECTOR_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
