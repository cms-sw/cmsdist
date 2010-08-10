### RPM external elementtree-toolfile 1.0
Requires: elementtree
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/elementtree.xml
<tool name="elementtree" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <client>
    <environment name="ELEMENTTREE_BASE" default="@TOOL_ROOT@"/>
    <environment name="ELEMENTTREE_PYPATH" default="$ELEMENTTREE_BASE/share/lib/python@PYTHONV@/site-packages"/>
  </client>
  <runtime name="PYTHONPATH" value="$ELEMENTTREE_PYPATH" type="path"/>
  <use name="gccxml"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
