### RPM external pyminuit2-toolfile 1.0
Requires: pyminuit2
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pyminuit2.xml
<tool name="pyminuit2" version="@TOOL_VERSION@">
<client>
<environment name="PYMINUIT2_BASE" default="@TOOL_ROOT@"/>
</client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
# bla bla
