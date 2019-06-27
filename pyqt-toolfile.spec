### RPM external pyqt-toolfile 1.0
Requires: pyqt

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/pyqt.xml
<tool name="pyqt" version="@TOOL_VERSION@">
  <client>
    <environment name="PYQT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PYQT_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
# bla bla
