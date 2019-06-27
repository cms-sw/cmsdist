### RPM external pyquen-toolfile 1.0
Requires: pyquen
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pyquen.xml
<tool name="pyquen" version="@TOOL_VERSION@">
  <lib name="pyquen"/>
  <client>
    <environment name="PYQUEN_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYQUEN_BASE/lib"/>
  </client>
  <use name="pythia6"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
