### RPM external geneva-toolfile 1.0
Requires: geneva

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/geneva.xml
<tool name="geneva" version="@TOOL_VERSION@">
  <client>
    <environment name="GENEVA_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$GENEVA_BASE/bin"/>
    <environment name="LIBDIR" default="$GENEVA_BASE/lib"/>
    <environment name="INCLUDE" default="$GENEVA_BASE/include/Geneva"/>
  </client>
  <runtime name="PATH" value="$GENEVA_BASE/bin" type="path"/>
  <runtime name="GENEVA_DATA_DIR" value="$GENEVA_BASE/share/Geneva" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="python"/>
  <use name="py2-numpy"/>
  <use name="HepMC"/>
  <use name="lhapdf"/>
%ifarch x86_64
  <use name="openloops"/>
%endif
  <use name="gsl"/>
  <use name="boost"/>
  <use name="pythia8"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
