### RPM external fastjet-toolfile 2.0
%define base_package %(echo %{n} | sed 's|-toolfile||')
%define base_package_uc %(echo %{base_package} | tr '[a-z-]' '[A-Z_]')
%{expand:%(for v in %{package_vectorization}; do echo Requires: %{base_package}_$v; done)}
Requires: %{base_package}
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%{base_package}.xml
  <tool name="%{base_package}" version="@TOOL_VERSION@">
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
EOF_TOOLFILE
for v in $(echo %{package_vectorization} | tr '[a-z-]' '[A-Z_]')  ; do
  r=`eval echo \\$%{base_package_uc}_${v}_ROOT`
  echo "    <environment name=\"${v}_LIBDIR\" default=\"${r}/lib\" type=\"path\"/>" >> %i/etc/scram.d/%{base_package}.xml
done
cat << \EOF_TOOLFILE >>%i/etc/scram.d/%{base_package}.xml
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
    <runtime name="PYTHON27PATH" value="$FASTJET_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>
EOF_TOOLFILE
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
