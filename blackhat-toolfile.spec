### RPM external blackhat-toolfile 1.0
Requires: blackhat

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/blackhat.xml
<tool name="blackhat" version="@TOOL_VERSION@">
<lib name="Ampl_eval"/>
<lib name="BG"/>
<lib name="BH"/>
<lib name="BHcore"/>
<lib name="CutPart"/>
<lib name="Cut_wCI"/>
<lib name="Cuteval"/>
<lib name="Integrals"/>
<lib name="Interface"/>
<lib name="OLA"/>
<lib name="RatPart"/>
<lib name="Rateval"/>
<lib name="Spinors"/>
<lib name="assembly"/>
<lib name="ratext"/>
<client>
<environment name="BLACKHAT_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$BLACKHAT_BASE/lib/blackhat"/>
<environment name="INCLUDE" default="$BLACKHAT_BASE/include"/>
</client>
<use name="qd"/>
<runtime name="WORKER_DATA_PATH" value="$BLACKHAT_BASE/share/blackhat/datafiles/" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
