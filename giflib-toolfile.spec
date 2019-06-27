### RPM external giflib-toolfile 1.0
Requires: giflib

%prep
%build
%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE > %{i}/etc/scram.d/giflib.xml
  <tool name="giflib" version="@TOOL_VERSION@">
    <info url="http://giflib.sourceforge.net"/>
    <lib name="gif"/>
    <client>
      <environment name="GIFLIB_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$GIFLIB_BASE/lib"/>
      <environment name="INCLUDE" default="$GIFLIB_BASE/include"/>
    </client>
    <runtime name="PATH" value="$GIFLIB_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
