GEANT4_VECGEOM=""
if grep VECGEOM_ROOT ${TOOL_ROOT}/etc/profile.d/dependencies-setup.sh >/dev/null 2>&1  ; then
  GEANT4_VECGEOM='<use name="vecgeom"/>'
fi
export GEANT4_VECGEOM

