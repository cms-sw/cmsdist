### RPM external dd4hep %{dd4hep_version}

## IMPORT dd4hep-common

%build
export BOOST_ROOT
CMAKE_ARGS="-DCMAKE_INSTALL_PREFIX='%{i}' \
      -DBoost_NO_BOOST_CMAKE=ON \
      -DDD4HEP_USE_XERCESC=ON \
      -DXERCESC_ROOT_DIR=${XERCES_C_ROOT} \
      -DDD4HEP_USE_PYROOT=ON \
      -DCMAKE_CXX_STANDARD=17 \
      -DCMAKE_BUILD_TYPE=Release \
      -DDD4HEP_USE_GEANT4_UNITS=ON \
      -DCMAKE_PREFIX_PATH=${CLHEP_ROOT};${XERCES_C_ROOT}"

#Build normal Shared D4Hep without Geant4
rm -rf ../build; mkdir ../build; cd ../build
cmake $CMAKE_ARGS -DBUILD_SHARED_LIBS=ON ../%{n}-%{realversion}
make %{makeprocesses} VERBOSE=1
make install

%install

%post
%{relocateConfig}bin/*.sh
