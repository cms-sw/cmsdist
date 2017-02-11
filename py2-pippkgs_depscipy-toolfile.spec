### RPM external py2-pippkgs_depscipy-toolfile 1.0
Requires: py2-pippkgs_depscipy
BuildRequires: python
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pippkgs_depscipy.xml
<tool name="py2-pippkgs_depscipy" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_PIPPKGS_DEPSCIPY" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_PIPPKGS_DEPSCIPY/@PYTHON_LIB_SITE_PACKAGES@" type="path"/>
  <runtime name="PATH" value="$PY2_PIPPKGS_DEPSCIPY/bin" type="path"/>
</tool>
EOF_TOOLFILE

export PYTHON_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
