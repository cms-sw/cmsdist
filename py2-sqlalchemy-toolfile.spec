### RPM external py2-sqlalchemy-toolfile 1.0
Requires: py2-sqlalchemy

%define pythonver %(echo %{allpkgreqs} | tr ' ' '\\n' | grep ^external/python/ | cut -d/ -f3 | cut -d. -f 1,2)
%define sqlalver %(echo %{allpkgreqs} | tr ' ' '\\n' | grep ^external/py2-sqlalchemy/ | cut -d/ -f3 | cut -d- -f 1)
%define pyArch %(uname -m)

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-sqlalchemy.xml
<tool name="py2-sqlalchemy" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_SQLALCHEMY_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHON27PATH" value="$PY2_SQLALCHEMY_BASE/lib/python@PYTHONV@/site-packages/SQLAlchemy-%{sqlalver}-py%{pythonver}-linux-%{pyArch}.egg" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post

