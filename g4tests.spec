### RPM external g4tests 1.0
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
%define GDMLSchema http://service-spi.web.cern.ch/service-spi/app/releases/GDML/GDML_2_8_0/src/GDMLSchema
Source0: http://cern.ch/vnivanch/ParFullCMS.tar.gz
Source1: %{GDMLSchema}/gdml.xsd
Source2: %{GDMLSchema}/gdml_core.xsd
Source3: %{GDMLSchema}/gdml_define.xsd
Source4: %{GDMLSchema}/gdml_extensions.xsd
Source5: %{GDMLSchema}/gdml_materials.xsd
Source6: %{GDMLSchema}/gdml_parameterised.xsd
Source7: %{GDMLSchema}/gdml_replicas.xsd
Source8: %{GDMLSchema}/gdml_solids.xsd

%if "%mic" != "true"
BuildRequires: cmake
%endif

Requires: geant4

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep

%setup -n ParFullCMS
perl -p -i -e "s|%{GDMLSchema}/|file:%i/GDMLSchema/|" cms.gdml

%build

rm -rf ../build; mkdir ../build; cd ../build

cmake ../ParFullCMS -DCMAKE_INSTALL_PREFIX:PATH="%i" -DGeant4_DIR=$GEANT4_ROOT/lib*/Geant4-* -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%if "%mic" == "true"
  -DCMAKE_CXX_COMPILER="icpc" \
  -DCMAKE_CXX_FLAGS="-mmic" \
  -DCMAKE_C_COMPILER="icc" \
  -DCMAKE_C_FLAGS="-mmic"
%else
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_CXX_FLAGS="%cms_cxxflags"
%endif

make %makeprocesses VERBOSE=1

%install
mkdir %i/GDMLSchema
cp cms.gdml  %i/
cp %_sourcedir/*.xsd %i/GDMLSchema

cd ../build
make install

%post
%{relocateConfig}cms.gdml
