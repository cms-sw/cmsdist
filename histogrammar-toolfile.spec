### RPM external histogrammar-toolfile 1.0
Requires: histogrammar
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/histogrammar.xml
<tool name="histogrammar" version="@TOOL_VERSION@">
  <client>
    <environment name="HISTOGRAMMAR_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$HISTOGRAMMAR_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
  <use name="py2-numpy"/>
  <use name="py2-pandas"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
