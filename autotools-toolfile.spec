### RPM external autotools-toolfile 1.0
Requires: autotools

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/autotools.xml
<tool name="autotools" version="@TOOL_VERSION@">
<lib name="ltdl"/>
<client>
<environment name="AUTOTOOLS_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$AUTOTOOLS_BASE/lib"/>
<environment name="INCLUDE" default="$AUTOTOOLS_BASE/include"/>
</client>
<runtime name="PATH" value="$AUTOTOOLS_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post



