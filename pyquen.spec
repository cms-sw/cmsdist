### RPM external pyquen 1.5.4

Source: http://lokhtin.web.cern.ch/lokhtin/%{n}/%{n}-%{realversion}.tar.gz

BuildRequires: cmake gmake

Requires: pythia6 lhapdf


%prep
%setup -q -n %{n}-%{realversion}

%build

cmake . -DCMAKE_INSTALL_PREFIX=%i \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DPYTHIA6_DIR=${PYTHIA6_ROOT} \
  -DLHAPDF_ROOT_DIR=${LHAPDF_ROOT}

cmake --build . --clean-first -- %{makeprocesses} VERBOSE=1

%install

cmake --build . --target install -- %{makeprocesses} VERBOSE=1
