### RPM external professor-toolfile 1.0
Requires: professor
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/professor.xml
<tool name="professor" version="@TOOL_VERSION@">
<client>
<environment name="PROFESSOR_BASE" default="@TOOL_ROOT@"/>
</client>
<runtime name="PATH" value="$PROFESSOR_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
# bla bla
