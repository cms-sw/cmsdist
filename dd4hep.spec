### RPM external dd4hep v01-23x
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto

%define tag 5c3b494f047ee025b2e32303c16ad854bfbb342d
%define branch master
%define github_user AIDASoft
%define keep_archives true

Source: git+https://github.com/%{github_user}/DD4hep.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: root boost clhep xerces-c geant4

%define build_flags -fPIC %{?arch_build_flags} %{?lto_build_flags} %{?pgo_build_flags}

%define cmake_fixed_args \\\
  -DCMAKE_INSTALL_PREFIX='%{i}' \\\
  -DCMAKE_CXX_FLAGS="%{build_flags}" \\\
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \\\
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \\\
  -DBoost_NO_BOOST_CMAKE=ON \\\
  -DDD4HEP_USE_XERCESC=ON \\\
  -DDD4HEP_USE_PYROOT=ON \\\
  -DCMAKE_AR=$(which gcc-ar) \\\
  -DCMAKE_RANLIB=$(which gcc-ranlib) \\\
  -DCMAKE_CXX_STANDARD=17 \\\
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \\\
  -DDD4HEP_USE_GEANT4_UNITS=ON \\\
  -DXERCESC_ROOT_DIR=${XERCES_C_ROOT} \\\
  -DCMAKE_PREFIX_PATH="${CLHEP_ROOT};${XERCES_C_ROOT}"

%prep

%setup -n %{n}-%{realversion}

%build

export BOOST_ROOT

#Build normal Shared D4Hep without Geant4
rm -rf ../build; mkdir ../build; cd ../build
cmake %{cmake_fixed_args} -DBUILD_SHARED_LIBS=ON ../%{n}-%{realversion}
make %{makeprocesses} VERBOSE=1
make install

#Building DDG4 static
rm -rf ../build-g4; mkdir ../build-g4; cd ../build-g4
cmake %{cmake_fixed_args} -DBUILD_SHARED_LIBS=OFF -DDD4HEP_USE_GEANT4=ON ../%{n}-%{realversion}
cd DDG4
make %{makeprocesses} VERBOSE=1
for lib in $(ls ../lib/libDDG4*.a | sed 's|.a$||'); do
  mv ${lib}.a %i/lib/${lib}-static.a
done
mv ../../%{n}-%{realversion}/DDG4/include/DDG4 %i/include

%install

%post
%{relocateConfig}bin/*.sh
