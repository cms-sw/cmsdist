### RPM external thepeg-toolfile 2.1
Requires: thepeg
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/thepeg.xml
<tool name="thepeg" version="@TOOL_VERSION@">
  <lib name="ThePEG"/>
  <lib name="LesHouches"/>
  <client>
    <environment name="THEPEG_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$THEPEG_BASE/lib/ThePEG"/>
    <environment name="INCLUDE" default="$THEPEG_BASE/include"/>
  </client>
  <runtime name="THEPEGPATH" value="$THEPEG_BASE/share/ThePEG"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="lhapdf"/>
  <use name="gsl"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

