### RPM external g4tests-toolfile 1.0
Requires: g4tests

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/g4tests.xml
<tool name="g4tests" version="@TOOL_VERSION@">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <client>
    <environment name="G4TESTS_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$G4TESTS_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
