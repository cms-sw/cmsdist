### RPM external rivet-toolfile 1.0
Requires: rivet

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/rivet.xml
<tool name="rivet" version="@TOOL_VERSION@">
<lib name="rivet"/>
<client>
<environment name="RIVET_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$RIVET_BASE/lib"/>
<environment name="INCLUDE" default="$RIVET_BASE/include"/>
<environment name="PDFPATH" default="$RIVET_BASE/share"/>
</client>
<runtime name="PATH" value="$RIVET_BASE/bin"/>
<runtime name="LD_LIBRARY_PATH" value="$RIVET_BASE/lib"/>
<runtime name="PYTHONPATH" value="$RIVET_BASE/lib/python2.6/site-packages"/>
<runtime name="RIVET_ANALYSIS_PATH" value="$RIVET_BASE/lib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

