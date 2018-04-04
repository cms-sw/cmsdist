### RPM external pyqt-toolfile 1.0
Requires: pyqt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pyqt.xml
<tool name="pyqt" version="@TOOL_VERSION@">
  <info url="http://www.riverbankcomputing.co.uk/software/pyqt/intro"/>
  <client>
    <environment name="PYQT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <use name="python"/>
  <use name="qt"/>
  <use name="sip"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
