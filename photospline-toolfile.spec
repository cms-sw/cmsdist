### RPM external photospline-toolfile 1.0
Requires: photospline
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/photospline.xml
<tool name="photospline" version="@TOOL_VERSION@">
  <info url="http://www..org"/>
  <lib name="photospline"/>
  <client>
    <environment name="PHOTOSPLINE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PHOTOSPLINE_BASE/lib"/>
    <environment name="INCLUDE" default="$PHOTOSPLINE_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="py2-matplotlib"/>
  <use name="gsl"/>
  <use name="lapack"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
