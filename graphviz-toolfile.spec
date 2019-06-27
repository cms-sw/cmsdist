### RPM external graphviz-toolfile 1.0
Requires: graphviz
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/graphviz.xml
<tool name="graphviz" version="@TOOL_VERSION@">
  <info url="http://www.research.att.com/sw/tools/graphviz/"/>
  <client>
    <environment name="GRAPHVIZ_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$GRAPHVIZ_BASE/bin" type="path"/>
  <use name="expat"/>
  <use name="zlib"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
