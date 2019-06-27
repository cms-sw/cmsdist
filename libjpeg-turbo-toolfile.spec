### RPM external libjpeg-turbo-toolfile 2.0
Requires: libjpeg-turbo
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/libjpg.xml
<tool name="libjpeg-turbo" version="@TOOL_VERSION@">
  <info url="http://libjpeg-turbo.virtualgl.org"/>
  <lib name="jpeg"/>
  <lib name="turbojpeg"/>
  <client>
    <environment name="LIBJPEG_TURBO_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBJPEG_TURBO_BASE/lib64"/>
    <environment name="INCLUDE" default="$LIBJPEG_TURBO_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="PATH" value="$LIBJPEG_TURBO_BASE/bin" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
