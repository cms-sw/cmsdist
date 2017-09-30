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

for pkg in $(grep '^[%]define  *builddirectpkgreqs  *external/' %{cmsroot}/SPECS/external/py2-pippkgs_depscipy/$PY2_PIPPKGS_DEPSCIPY_VERSION/spec | sed 's|.* builddirectpkgreqs *||' | tr ' ' '\n' | grep '/py2-')  ; do
  pk_name=$(echo $pkg | cut -d/ -f2)
  pk_ver=$(echo $pkg | cut -d/ -f3)
  echo "<tool name=\"$pk_name\" version=\"$pk_ver\">" > %{i}/etc/scram.d/$pk_name.xml
  echo "  <use name=\"py2-pippkgs_depscipy\"/>" >> %{i}/etc/scram.d/$pk_name.xml
  echo "</tool>" >> %{i}/etc/scram.d/$pk_name.xml
done

export PYTHON_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
