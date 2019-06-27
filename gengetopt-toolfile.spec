### RPM external gengetopt-toolfile 1.0
Requires: gengetopt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gengetopt.xml
<tool name="gengetopt" version="@TOOL_VERSION@">
  <client>
    <environment name="GENGETOPT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$GENGETOPT_BASE/bin" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
