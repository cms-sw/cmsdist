### RPM external igprof-toolfile 1.0
Requires: igprof
%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/igprof.xml
  <tool name="igprof" version="@TOOL_VERSION@">
    <info url="http://igprof.sourceforge.net/"/>
    <client>
      <environment name="IGPROF_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$IGPROF_BASE/lib"/>
    </client>
    <runtime name="PATH" value="$IGPROF_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
