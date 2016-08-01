### RPM external py2-scikit-learn-toolfile 1.0
Requires: py2-scikit-learn
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-scikit-learn.xml
<tool name="py2-scikit-learn" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2SCIKIT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2SCIKIT_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
  <use name="py2-numpy"/>
  <use name="py2-matplotlib"/>
  <use name="py2-scipy "/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post

