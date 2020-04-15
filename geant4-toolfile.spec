### RPM external geant4-toolfile 1.0
Requires: geant4

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/geant4.xml
<tool name="geant4" version="@TOOL_VERSION@">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <use name="geant4core"/>
  <use name="geant4vis"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/geant4core.xml
<tool name="geant4core" version="@TOOL_VERSION@">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4digits_hits"/>
  <lib name="G4error_propagation"/>
  <lib name="G4event"/>
  <lib name="G4geometry"/>
  <lib name="G4global"/>
  <lib name="G4graphics_reps"/>
  <lib name="G4intercoms"/>
  <lib name="G4interfaces"/>
  <lib name="G4materials"/>
  <lib name="G4parmodels"/>
  <lib name="G4particles"/>
  <lib name="G4persistency"/>
  <lib name="G4physicslists"/>
  <lib name="G4processes"/>
  <lib name="G4readout"/>
  <lib name="G4run"/>
  <lib name="G4tracking"/>
  <lib name="G4track"/>
  <lib name="G4analysis"/>
  <flags CXXFLAGS="-ftls-model=global-dynamic -pthread"/>
  <client>
    <environment name="GEANT4CORE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GEANT4CORE_BASE/lib"/>
    <environment name="G4LIB" value="$LIBDIR"/>
    <environment name="INCLUDE" default="$GEANT4CORE_BASE/include/Geant4"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$INCLUDE" type="path"/>
  <flags cppdefines="GNU_GCC G4V9"/>
  <use name="clhep"/>
  <use name="vecgeom"/>
  <use name="zlib"/>
  <use name="expat"/>
  <use name="xerces-c"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/geant4static.xml
<tool name="geant4static" version="@TOOL_VERSION@">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="geant4-static"/>
  <flags CXXFLAGS="-ftls-model=global-dynamic -pthread"/>
  <client>
    <environment name="GEANT4STATIC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GEANT4STATIC_BASE/lib/archive"/>
  </client>
  <use name="clhep"/>
  <use name="vecgeom"/>
  <use name="zlib"/>
  <use name="expat"/>
  <use name="xerces-c"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/geant4vis.xml
<tool name="geant4vis" version="@TOOL_VERSION@">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4FR"/>
  <lib name="G4modeling"/>
  <lib name="G4RayTracer"/>
  <lib name="G4Tree"/>
  <lib name="G4visHepRep"/>
  <lib name="G4vis_management"/>
  <lib name="G4visXXX"/>
  <lib name="G4VRML"/>
  <lib name="G4GMocren"/>
  <use name="geant4core"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
