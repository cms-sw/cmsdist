### RPM external python-toolfile 1.0
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
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="PYTHON_VALGRIND_SUPP" value="$PYTHON_BASE/share/valgrind/valgrind-python.supp" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
# bla bla
