### RPM external lwtnn-toolfile 1.0
Requires: lwtnn
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/lwtnn.xml
<tool name="lwtnn" version="@TOOL_VERSION@">
  <info url="https://github.com/lwtnn/lwtnn"/>
  <lib name="lwtnn"/>
  <client>
    <environment name="LWTNN_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LWTNN_BASE/lib"/>
    <environment name="INCLUDE" default="$LWTNN_BASE/include"/>
  </client>
  <runtime name="PATH" value="$LWTNN_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="eigen"/>
  <use name="boost_system"/>  
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
