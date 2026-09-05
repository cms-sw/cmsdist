### RPM external sherpa3 3.0.5
Source: git+https://gitlab.com/sherpa-team/sherpa.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: hepmc3 lhapdf blackhat fastjet openmpi rivet pythia8 libzip python3
BuildRequires: cmake swig

Patch0: sherpa-3.0.5-versioning
#Fix -Werror=reorder in Particle_Info constructor (init order m_hmass/m_radius)
Patch1: sherpa-3.0.5-reorder

%{!?without_openloops:Requires: openloops}

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1

%build
rm -rf build && mkdir build

cmake -S . -B build \
  -DCMAKE_INSTALL_PREFIX=%i \
  -DSHERPA_ENABLE_VERSIONING=ON \
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
  -DSHERPA_ENABLE_PYTHIA8=ON -DPYTHIA8_DIR=$PYTHIA8_ROOT \
  -DSHERPA_ENABLE_RECOLA=OFF \
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
sed -i -e 's|^#!/.*|#!/usr/bin/env python3|' %{i}/bin/Sherpa3-generate-model

%post
%{relocateConfig}bin/Sherpa3-config
%{relocateConfig}bin/Sherpa3-generate-model
%{relocateConfig}share/SHERPA-MC3/makelibs
%{relocateConfig}include/SHERPA-MC3/ATOOLS/Org/CXXFLAGS*.H
%{relocateConfig}lib/python%{cms_python3_major_minor_version}/site-packages/ufo_interface/parser.py
