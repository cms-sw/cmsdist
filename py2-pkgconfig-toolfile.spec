### RPM external py2-pkgconfig-toolfile 1.0
Requires: py2-pkgconfig
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-pkgconfig.xml
<tool name="py2-pkgconfig" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_PKGCONFIG_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_PKGCONFIG_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post


