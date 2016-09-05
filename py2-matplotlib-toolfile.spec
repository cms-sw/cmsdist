### RPM external py2-matplotlib-toolfile 1.0
Requires: py2-matplotlib
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-matplotlib.xml
<tool name="py2-matplotlib" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_MATPLOTLIB_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_MATPLOTLIB_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
  <use name="zlib"/>
  <use name="libpng"/>
  <use name="py2-numpy"/>
  <use name="py2-python-dateutil"/>
  <use name="py2-cycler"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
## IMPORT scram-tools-post
