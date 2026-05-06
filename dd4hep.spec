### RPM external dd4hep v01-31-0x
%define tag 4990888b50e29a5dc0ff65fc3a6fdf17205192a5
%define branch master
%define github_user AIDASoft

Source: git+https://github.com/%{github_user}/DD4hep.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
## INCLUDE geant4-deps

Requires: root boost geant4
# ROOT uses the json package, and seems to require that it be availble also when other packages use ROOT
Requires: json

%define cmake_fixed_args \\\
  -DCMAKE_INSTALL_PREFIX='%{i}' \\\
  -DCMAKE_CXX_FLAGS="%{build_flags}" \\\
  -DBoost_NO_BOOST_CMAKE=ON \\\
  -DDD4HEP_USE_XERCESC=ON \\\
  -DCMAKE_AR=$(which gcc-ar) \\\
  -DCMAKE_RANLIB=$(which gcc-ranlib) \\\
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \\\
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \\\
  -DDD4HEP_USE_GEANT4_UNITS=ON \\\
  -DXERCESC_ROOT_DIR=${XERCES_C_ROOT} \\\
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

%prep

%setup -n %{n}-%{realversion}

%build

export BOOST_ROOT

#Build normal Shared D4Hep without Geant4
rm -rf ../build; mkdir ../build; cd ../build
cmake %{cmake_fixed_args} -DBUILD_SHARED_LIBS=ON -DDD4HEP_USE_GEANT4=OFF ../%{n}-%{realversion}
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
