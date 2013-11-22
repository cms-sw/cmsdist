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
%if "%mic" == "true"
    <environment name="PYTHONHOST_BASE" default="/usr"/>
%endif
    <environment name="PYTHON_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHON_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHON_BASE/include/python@PYTHONV@"/>
    <environment name="PYTHON_COMPILE" default="$PYTHON_BASE/lib/python@PYTHONV@/compileall.py"/>
  </client>
%if "%mic" == "true"
  <runtime name="MIC_SRTOPT_PATH" value="$PYTHON_BASE/bin" type="path"/>
%else
  <runtime name="PATH" value="$PYTHON_BASE/bin" type="path"/>
%endif
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
