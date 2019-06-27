### RPM external gnuplot-toolfile 1.0
Requires: gnuplot

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/gnuplot.xml
  <tool name="gnuplot" version="@TOOL_VERSION@">
    <info url="http://gnuplot.sourceforge.net"/>
    <client>
      <environment name="GNUPLOT_BASE" default="@TOOL_ROOT@"/>
    </client>
    <runtime name="PATH" value="$GNUPLOT_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
