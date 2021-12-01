### RPM external hydjet2 2.x.y 

Source: http://cern.ch/lokhtin/hydjet++/%{n}.tar.gz

BuildRequires: cmake gmake

Requires: pyquen pythia6 lhapdf root


%prep
%setup -q -n %{n}

%build

cmake . -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_BUILD_TYPE=Release -DPYQUEN_DIR=${PYQUEN_ROOT} -DPYTHIA6_DIR=${PYTHIA6_ROOT} -DLHAPDF_ROOT_DIR=${LHAPDF_ROOT} -DROOTSYS=${ROOT_ROOT}
cmake --build . --clean-first -- %{makeprocesses}

%install

cmake --build . --target install -- %{makeprocesses}
