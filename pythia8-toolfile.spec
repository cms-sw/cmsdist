### RPM external pythia8-toolfile 1.0
Requires: pythia8

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/pythia8.xml
<tool name="pythia8" version="@TOOL_VERSION@">
  <client>
    <environment name="PYTHIA8_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PYTHIA8_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
