### RPM external yoda-toolfile 1.0
Requires: yoda
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/yoda.xml
<tool name="yoda" version="@TOOL_VERSION@">
  <lib name="YODA"/>
  <client>
    <environment name="YODA_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$YODA_BASE/lib"/>
    <environment name="INCLUDE" default="$YODA_BASE/include"/>
  </client>
  <use name="root_cxxdefaults"/>
  <runtime name="PATH"       value="$YODA_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
## IMPORT scram-tools-post
# bla bla
