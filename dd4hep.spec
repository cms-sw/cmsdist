### RPM external dd4hep v01-10x

%define tag 88e428e1c81b1d7a51f9d046bd116ae23a7fb992
%define branch cms/master/052a2b2
%define github_user cms-externals
%define keep_archives true

Source: git+https://github.com/%{github_user}/DD4hep.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: root boost clhep xerces-c geant4
Patch0: dd4hep-build-static

%prep

%setup -n %{n}-%{realversion}

%build

export BOOST_ROOT
CMAKE_ARGS="-DCMAKE_INSTALL_PREFIX='%{i}'
      -DBoost_NO_BOOST_CMAKE=ON
      -DCMAKE_PREFIX_PATH=${CLHEP_ROOT}
      -DDD4HEP_USE_XERCESC=ON
      -DXERCESC_ROOT_DIR=${XERCES_C_ROOT}
      -DDD4HEP_USE_PYROOT=ON
      -DCMAKE_CXX_STANDARD=17
      -DCMAKE_BUILD_TYPE=Release"

#Build normal Shared D4Hep without Geant4
rm -rf ../build; mkdir ../build; cd ../build
cmake $CMAKE_ARGS ../%{n}-%{realversion}
make %{makeprocesses} VERBOSE=1
make install

#Building DDG4 static
cd %{_builddir}/%{n}-%{realversion}
patch -p1 < %{_sourcedir}/dd4hep-build-static
rm -rf ../build-g4; mkdir ../build-g4; cd ../build-g4
cmake $CMAKE_ARGS -DDD4HEP_USE_GEANT4=ON ../%{n}-%{realversion}
cd DDG4
make %{makeprocesses} VERBOSE=1
for lib in $(ls ../lib/libDDG4*.a | sed 's|.a$||'); do
  mv ${lib}.a %i/lib/${lib}-static.a
done
mv ../../%{n}-%{realversion}/DDG4/include/DDG4 %i/include

%install

%post
%{relocateConfig}*.cmake
%{relocateConfig}bin/*.sh
%{relocateConfig}bin/*.csh
# bla bla
