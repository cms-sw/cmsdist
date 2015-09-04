### RPM external py2-docopt-toolfile 1.0
Requires: py2-docopt
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-docopt.xml
<tool name="py2-docopt" version="@TOOL_VERSION@">
  <info url="https://github.com/docopt/docopt"/>
  <client>
    <environment name="PY2_DOCOPT" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_DOCOPT/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_DOCOPT/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
