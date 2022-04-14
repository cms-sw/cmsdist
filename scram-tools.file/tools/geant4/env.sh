GEANT4_VECGEOM=""
if grep VECGEOM_ROOT ${TOOL_ROOT}/etc/profile.d/dependencies-setup.sh >/dev/null 2>&1  ; then
  GEANT4_VECGEOM='<use name="vecgeom"/><flags CXXFLAGS="-DG4GEOM_USE_USOLIDS"/>'
fi
export GEANT4_VECGEOM

