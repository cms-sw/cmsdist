## IMPORT dd4hep-common
### RPM external dd4hep-geant4 %{dd4hep_version}

Requires: geant4

%prep
%setup -n dd4hep-%{realversion}

%build
export BOOST_ROOT
#Building DDG4 static
rm -rf ../build-g4; mkdir ../build-g4; cd ../build-g4
cmake $CMAKE_ARGS -DBUILD_SHARED_LIBS=OFF -DDD4HEP_USE_GEANT4=ON ../%{n}-%{realversion}
cd DDG4
make %{makeprocesses} VERBOSE=1
for lib in $(ls ../lib/libDDG4*.a | sed 's|.a$||'); do
  mv ${lib}.a %i/lib/${lib}-static.a
done
mv ../../%{n}-%{realversion}/DDG4/include/DDG4 %i/include

%install

%post
%{relocateConfig}bin/*.sh
