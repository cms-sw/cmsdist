### RPM external vecgeom-toolfile 4.0
%define base_package %(echo %{n} | sed 's|-toolfile||')
%define base_package_uc %(echo %{base_package} | tr '[a-z-]' '[A-Z_]')
%{expand:%(for v in %{package_vectorization}; do echo Requires: %{base_package}_$v; done)}
Requires: %{base_package}
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
    <environment name="INCLUDE" default="$VECGEOM_INTERFACE_BASE/include/VecGeom"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$VECGEOM_INTERFACE_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$VECGEOM_INTERFACE_BASE/include/VecGeom" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%{base_package}.xml
<tool name="%{base_package}" version="@TOOL_VERSION@">
  <info url="https://gitlab.cern.ch/VecGeom/VecGeom"/>
  <lib name="vecgeom"/>
  <client>
    <environment name="VECGEOM_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$VECGEOM_BASE/lib"/>
EOF_TOOLFILE
for v in $(echo %{package_vectorization} | tr '[a-z-]' '[A-Z_]')  ; do
  r=`eval echo \\$%{base_package_uc}_${v}_ROOT`
  echo "    <environment name=\"${v}_LIBDIR\" default=\"${r}/lib\" type=\"path\"/>" >> %i/etc/scram.d/%{base_package}.xml
done
cat << \EOF_TOOLFILE >>%i/etc/scram.d/%{base_package}.xml
  </client>
  <use name="vecgeom_interface"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
