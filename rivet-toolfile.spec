### RPM external rivet-toolfile 1.0
Requires: rivet

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/rivet.xml
<tool name="rivet" version="@TOOL_VERSION@">
<lib name="Rivet"/>
<client>
<environment name="RIVET_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$RIVET_BASE/lib"/>
<environment name="INCLUDE" default="$RIVET_BASE/include"/>
</client>
<runtime name="PATH" value="$RIVET_BASE/bin" type="path"/>
<runtime name="PYTHONPATH" value="$RIVET_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
<runtime name="RIVET_ANALYSIS_PATH" value="$RIVET_BASE/lib" type="path"/>
<runtime name="PDFPATH" default="$RIVET_BASE/share" type="path"/>
<runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
<use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post


