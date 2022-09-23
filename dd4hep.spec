### RPM external dd4hep v01-19x
## INCLUDE compilation_flags

%define tag cc335b34e9eb2825ab18e20c531be813a92d141f
%define branch master
%define github_user AIDASoft
%define keep_archives true

Source: git+https://github.com/%{github_user}/DD4hep.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: root boost clhep xerces-c geant4

%prep

%setup -n %{n}-%{realversion}

%build
%if "%{?arch_build_flags}"
%define build_flags -fPIC %{arch_build_flags} %{lto_build_flags}
%else
%define build_flags -fPIC %{lto_build_flags}
%endif

export BOOST_ROOT
CMAKE_ARGS="-DCMAKE_INSTALL_PREFIX='%{i}' \
      -DBoost_NO_BOOST_CMAKE=ON \
      -DDD4HEP_USE_XERCESC=ON \
      -DXERCESC_ROOT_DIR=${XERCES_C_ROOT} \
      -DDD4HEP_USE_PYROOT=ON \
      -DCMAKE_AR=$(which gcc-ar) \
      -DCMAKE_RANLIB=$(which gcc-ranlib) \
      -DCMAKE_CXX_STANDARD=17 \
      -DCMAKE_BUILD_TYPE=Release \
      -DDD4HEP_USE_GEANT4_UNITS=ON \
      -DCMAKE_PREFIX_PATH=${CLHEP_ROOT};${XERCES_C_ROOT}"

#Build normal Shared D4Hep without Geant4
rm -rf ../build; mkdir ../build; cd ../build
cmake $CMAKE_ARGS \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_CXX_FLAGS="%{build_flags}" \
      -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
      -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
      ../%{n}-%{realversion}
make %{makeprocesses} VERBOSE=1
make install

#Building DDG4 static
rm -rf ../build-g4; mkdir ../build-g4; cd ../build-g4
cmake $CMAKE_ARGS \
      -DBUILD_SHARED_LIBS=OFF \
      -DDD4HEP_USE_GEANT4=ON  \
      -DCMAKE_CXX_FLAGS="%{build_flags}" \
      -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
      -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
      ../%{n}-%{realversion}
cd DDG4
make %{makeprocesses} VERBOSE=1
for lib in $(ls ../lib/libDDG4*.a | sed 's|.a$||'); do
  mv ${lib}.a %i/lib/${lib}-static.a
done
mv ../../%{n}-%{realversion}/DDG4/include/DDG4 %i/include

%install

%post
%{relocateConfig}bin/*.sh
