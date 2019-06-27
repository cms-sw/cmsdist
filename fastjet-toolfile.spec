### RPM external fastjet-toolfile 1.0
Requires: fastjet
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/fastjet.xml
  <tool name="fastjet" version="@TOOL_VERSION@">
    <info url="http://fastjet.fr"/>
    <lib name="fastjetplugins"/>
    <lib name="fastjettools"/>
    <lib name="siscone"/>
    <lib name="siscone_spherical"/>
    <lib name="fastjet"/>
    <client>
      <environment name="FASTJET_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$FASTJET_BASE/lib"/>
      <environment name="INCLUDE" default="$FASTJET_BASE/include"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
    <runtime name="PYTHON27PATH" value="$FASTJET_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>
EOF_TOOLFILE
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
# bla bla
