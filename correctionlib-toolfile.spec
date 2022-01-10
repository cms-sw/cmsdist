### RPM external correctionlib-toolfile 1.1
Requires: correctionlib
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/correctionlib.xml
<tool name="correctionlib" version="@TOOL_VERSION@">
  <lib name="correctionlib"/>
  <client>
    <environment name="CORRECTIONLIB_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$CORRECTIONLIB_BASE/@PYTHON_LIB_SITE_PACKAGES@/correctionlib/include"/>
    <environment name="LIBDIR" default="$CORRECTIONLIB_BASE/@PYTHON_LIB_SITE_PACKAGES@/correctionlib/lib"/>
    <environment name="BINDIR" default="$CORRECTIONLIB_BASE/bin"/>
  </client>
  <runtime name="PATH" default="$BINDIR" type="path"/>
</tool>
EOF_TOOLFILE

export PYTHON_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
