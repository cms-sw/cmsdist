### RPM external rivet-toolfile 1.0
%define base_package %(echo %{n} | sed 's|-toolfile||')
%define base_package_uc %(echo %{base_package} | tr '[a-z-]' '[A-Z_]')
%{expand:%(for v in %{package_vectorization}; do echo Requires: %{base_package}_$v; done)}
Requires: %{base_package}

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/rivet.xml
<tool name="rivet" version="@TOOL_VERSION@">
<lib name="Rivet"/>
<client>
<environment name="RIVET_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$RIVET_BASE/lib"/>
<environment name="INCLUDE" default="$RIVET_BASE/include"/>
EOF_TOOLFILE
for v in $(echo %{package_vectorization} | tr '[a-z-]' '[A-Z_]')  ; do
  r=`eval echo \\$%{base_package_uc}_${v}_ROOT`
  echo "    <environment name=\"${v}_LIBDIR\" default=\"${r}/lib\" type=\"path\"/>" >> %i/etc/scram.d/rivet.xml
done
cat << \EOF_TOOLFILE >>%i/etc/scram.d/rivet.xml
</client>
<runtime name="PATH" value="$RIVET_BASE/bin" type="path"/>
<runtime name="RIVET_ANALYSIS_PATH" value="$RIVET_BASE/lib/Rivet" type="path"/>
<runtime name="RIVET_DATA_PATH" value="$RIVET_BASE/share/Rivet" type="path"/>
<runtime name="PDFPATH" default="$RIVET_BASE/share" type="path"/>
<runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
<runtime name="TEXMFHOME" value="$RIVET_BASE/share/Rivet/texmf" type="path"/>
<use name="hepmc"/>
<use name="fastjet"/>
<use name="fastjet-contrib"/>
<use name="gsl"/>
<use name="yoda"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post


