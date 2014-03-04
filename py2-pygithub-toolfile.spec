### RPM external py2-pygithub-toolfile 1.0
Requires: py2-pygithub
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pygithub.xml
<tool name="py-pygithub" version="@TOOL_VERSION@">
  <info url="https://github.com/jacquev6/PyGithub"/>
  <client>
    <environment name="PY2_PYGITHUB" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PYGITHUB/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PYGITHUB/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
