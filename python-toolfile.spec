### RPM external python-toolfile 1.0
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
Requires: python
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/python.xml
<tool name="python" version="@TOOL_VERSION@">
  <lib name="python@PYTHONV@"/>
  <client>
    <environment name="PYTHON_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHON_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHON_BASE/include/python@PYTHONV@"/>
    <environment name="PYTHON_COMPILE" default="$PYTHON_BASE/lib/python@PYTHONV@/compileall.py"/>
  </client>
  <runtime name="PATH" value="$PYTHON_BASE/bin" type="path"/>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

%if "%mic" == "true"
cat << \EOF_TOOLFILE >%i/etc/scram.d/pythonhost.xml
<tool name="pythonhost" version="@TOOL_VERSION@">
  <client>
    <environment name="PYTHONHOST_BASE" default="/usr"/>
  </client>
</tool>
EOF_TOOLFILE
%endif

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
