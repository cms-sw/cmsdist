### RPM external professor2-toolfile 2.0
Requires: professor2
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/professor2.xml
<tool name="professor2" version="@TOOL_VERSION@">
<client>
<environment name="PROFESSOR2_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$PROFESSOR2_BASE/lib"/>
</client>
<use name="py2-numpy"/>
<use name="root"/>
<use name="yoda"/>
<use name="eigen"/>
<runtime name="PATH" value="$PROFESSOR2_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
