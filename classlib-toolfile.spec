### RPM external classlib-toolfile 1.0
Requires: classlib

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/classlib.xml
  <tool name="classlib" version="@TOOL_VERSION@">
    <info url="http://cmsmac01.cern.ch/~lat/exports/"/>
    <client>
      <environment name="CLASSLIB_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$CLASSLIB_BASE/lib"/>
    </client>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
