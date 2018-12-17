### RPM external geneva 1.0-RC3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Source: git+https://stash.desy.de/scm/geneva/geneva-public.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: cmake gmake

Requires: python py2-setuptools py2-numpy gsl boost lhapdf hepmc openloops pythia8

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build
cmake ../%{n}-%{realversion} \
      -DCMAKE_INSTALL_PREFIX=%{i} \
      -DCMAKE_CXX_STANDARD=11 \
      -Dgsl_ROOT=${GSL_ROOT} \
      -Dboost_ROOT=${BOOST_ROOT} \
      -Dlhapdf_ROOT=${LHAPDF_ROOT} \
      -Dhepmc_ROOT=${HEPMC_ROOT} \
      -Dopenloops_ROOT=${OPENLOOPS_ROOT} \
      -Dpythia8_ROOT=${PYTHIA8_ROOT}

make %{makeprocesses}
make beamfunc-install-data LHAPDF_DATA_PATH=${LHAPDF_ROOT}/share/LHAPDF

%install
cd ../build
make install
cd %{i}/bin
sed -i '/#!/c\#!/usr/bin/env python' *
