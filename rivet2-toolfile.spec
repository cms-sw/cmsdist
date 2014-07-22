### RPM external rivet2-toolfile 1.0
Requires: rivet2

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/rivet2.xml
<tool name="rivet2" version="@TOOL_VERSION@">
<lib name="Rivet"/>
<client>
<environment name="RIVET2_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$RIVET2_BASE/lib"/>
<environment name="INCLUDE" default="$RIVET2_BASE/include"/>
</client>
<runtime name="PATH" value="$RIVET2_BASE/bin" type="path"/>
<runtime name="PYTHONPATH" value="$RIVET2_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
<runtime name="RIVET_ANALYSIS_PATH" value="$RIVET2_BASE/lib" type="path"/>
<runtime name="PDFPATH" default="$RIVET2_BASE/share" type="path"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post


