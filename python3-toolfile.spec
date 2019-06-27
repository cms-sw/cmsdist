### RPM external python3-toolfile 1.0
Requires: python3
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/python3.xml
<tool name="python3" version="@TOOL_VERSION@">
  <lib name="python@PYTHON3V@m"/>
  <client>
    <environment name="PYTHON3_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHON3_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHON3_BASE/include/python@PYTHON3V@m"/>
    <environment name="PYTHON3_COMPILE" default="$PYTHON3_BASE/lib/python@PYTHON3V@/compileall.py"/>
  </client>
  <runtime name="PATH" value="$PYTHON3_BASE/bin" type="path"/>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE


#  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
#  <use name="root_cxxdefaults"/>

export PYTHON3V=$(echo $PYTHON3_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
# bla bla
