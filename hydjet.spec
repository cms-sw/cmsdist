### RPM external hydjet 1.9.1

Source: http://cern.ch/lokhtin/hydro/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

Requires: pyquen pythia6 lhapdf


%prep
%setup -q -n %{n}-%{realversion}

%build

cmake . -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_BUILD_TYPE=Release -DPYQUEN_DIR=${PYQUEN_ROOT} -DPYTHIA6_DIR=${PYTHIA6_ROOT} -DLHAPDF_ROOT_DIR=${LHAPDF_ROOT}
cmake --build . --clean-first -- %{makeprocesses}

%install

cmake --build . --target install -- %{makeprocesses}
