### RPM external py2-pippkgs-toolfile 1.0
Requires: py2-pippkgs
BuildRequires: python
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pippkgs.xml
<tool name="py2-pippkgs" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_PIPPKGS" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_PIPPKGS/@PYTHON_LIB_SITE_PACKAGES@" type="path"/>
</tool>
EOF_TOOLFILE

export PYTHON_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
