### RPM external sigcpp-toolfile 1.0
Requires: sigcpp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/sigcpp.xml
<tool name="sigcpp" version="@TOOL_VERSION@">
  <lib name="sigc-2.0"/>
  <client>
    <environment name="SIGCPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$SIGCPP_BASE/lib"/>
    <environment name="INCLUDE" default="$SIGCPP_BASE/include/sigc++-2.0"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
