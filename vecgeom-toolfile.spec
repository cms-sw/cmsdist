### RPM external vecgeom-toolfile 1.0
Requires: vecgeom
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/vecgeom_interface.xml
<tool name="vecgeom_interface" version="@TOOL_VERSION@">
  <info url="https://gitlab.cern.ch/VecGeom/VecGeom"/>
  <client>
    <environment name="VECGEOM_INTERFACE_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$VECGEOM_INTERFACE_BASE/include"/>
  </client>
  <flags CPPDEFINES="VECGEOM_SCALAR"/>
  <flags CPPDEFINES="VECGEOM_REPLACE_USOLIDS"/>
  <flags CPPDEFINES="VECGEOM_NO_SPECIALIZATION"/>
  <flags CPPDEFINES="VECGEOM_USOLIDS"/>
  <flags CPPDEFINES="VECGEOM_INPLACE_TRANSFORMATIONS"/>
  <flags CPPDEFINES="VECGEOM_USE_INDEXEDNAVSTATES"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/vecgeom.xml
<tool name="vecgeom" version="@TOOL_VERSION@">
  <info url="https://gitlab.cern.ch/VecGeom/VecGeom"/>
  <lib name="vecgeom"/>
  <lib name="usolids"/>
  <client>
    <environment name="VECGEOM_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$VECGEOM_BASE/lib"/>
  </client>
  <use name="vecgeom_interface"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
