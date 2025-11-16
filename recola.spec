### RPM external recola 1.4.4
Source: https://recola.hepforge.org/downloads/%{n}-%{realversion}.tar.gz
Requires: collier
BuildRequires: cmake

%define keep_archives true

%prep
%setup -q -n recola-%{realversion}

%build
rm -rf build && mkdir build
cmake -S . -B build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -Dcollier_path=${COLLIER_ROOT} \
  -Dwith_smtests=ON
cmake --build build %{makeprocesses}


%install
cmake --install build
mv %{i}/lib/cmake %{i}/cmake
sed -i 's;^.*set(RECOLA_LIBRARY_DIR.*$;get_filename_component(RECOLA_LIBRARY_DIR "${CMAKE_CURRENT_LIST_DIR}/../lib" ABSOLUTE);' %{i}/cmake/recolaConfig.cmake
sed -i 's;^.*set(RECOLA_INCLUDE_DIR.*$;get_filename_component(RECOLA_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/../include" ABSOLUTE);' %{i}/cmake/recolaConfig.cmake
