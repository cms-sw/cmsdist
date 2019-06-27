### RPM external cppunit-toolfile 1.0
Requires: cppunit
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cppunit.xml
<tool name="cppunit" version="@TOOL_VERSION@">
  <lib name="cppunit"/>
  <client>
    <environment name="CPPUNIT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CPPUNIT_BASE/lib"/>
    <environment name="INCLUDE" default="$CPPUNIT_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
