### RPM external pyquen 1.5.3

Source: http://lokhtin.web.cern.ch/lokhtin/%{n}/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

Requires: pythia6 lhapdf


%prep
%setup -q -n %{n}-%{realversion}

%build

cmake . -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_BUILD_TYPE=Release -DPYTHIA6_DIR=${PYTHIA6_ROOT} -DLHAPDF_ROOT_DIR=${LHAPDF_ROOT}
cmake --build . --clean-first -- %{makeprocesses}

%install

cmake --build . --target install --clean-first -- %{makeprocesses}
