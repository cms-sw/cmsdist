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
<runtime name="PYTHONPATH" value="$PYMINUIT2_BASE/lib/python2.6/site-packages" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
