### RPM external sherpa 3.0.3
Source: git+https://gitlab.com/sherpa-team/sherpa.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: hepmc3 lhapdf blackhat fastjet openmpi recola rivet pythia8 gosam libzip
BuildRequires: cmake swig

%{!?without_openloops:Requires: openloops}

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf build && mkdir build

cmake -S . -B build \
  -DCMAKE_INSTALL_PREFIX=%i \
  -DSHERPA_ENABLE_MPI=ON -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DCMAKE_Fortran_COMPILER=mpifort \
  -DSHERPA_ENABLE_ANALYSIS=ON \
  -DSHERPA_ENABLE_EXAMPLES=ON \
  -DSHERPA_ENABLE_LIBZIP=ON -DLibZip_DIR=$LIBZIP_ROOT \
  -DSHERPA_ENABLE_GZIP=ON \
  -DSHERPA_ENABLE_HEPMC3=ON -DHEPMC3_DIR=$HEPMC3_ROOT -DSHERPA_ENABLE_HEPMC3_ROOT=OFF \
  -DSHERPA_ENABLE_LHAPDF=ON -DLHAPDF_DIR=$LHAPDF_ROOT -DSHERPA_ENABLE_INTERNAL_PDFS=OFF \
  -DSHERPA_ENABLE_BLACKHAT=ON -DBLACKHAT_DIR=$BLACKHAT_ROOT \
  ${OPENLOOPS_ROOT+-DSHERPA_ENABLE_OPENLOOPS=ON -DOPENLOOPS_DIR=$OPENLOOPS_ROOT} \
  -DSHERPA_ENABLE_ROOT=OFF \
  -DSHERPA_ENABLE_PYTHIA8=ON -DPYHIA8_DIR=$PYTHIA8_ROOT \
  -DSHERPA_ENABLE_RECOLA=OFF \
  -DSHERPA_ENABLE_GOSAM=ON -DGOSAM_DIR=$GOSAM_ROOT \
  -DSHERPA_ENABLE_RIVET=ON -DRIVET_DIR=$RIVET_ROOT \
  -DSHERPA_ENABLE_EWSUD=ON \
  -DSHERPA_ENABLE_PYTHON=ON \
  -DSHERPA_ENABLE_UFO=ON \
  -DSHERPA_ENABLE_THREADING=ON \
  -DSHERPA_ENABLE_DIHIGGS=OFF \
  -DSHERPA_ENABLE_MADLOOP=OFF \
  -DSHERPA_ENABLE_MCFM=OFF \
  -DSHERPA_ENABLE_TESTING=OFF \
  -DSHERPA_ENABLE_INTEGRATION_TESTS=OFF \
  -DSHERPA_ENABLE_BINRELOC=OFF
cmake --build build %{makeprocesses}

%install
cmake --install build
sed -i -e 's|^#!/.*|#!/usr/bin/env python3|' %{i}/bin/Sherpa-generate-model
