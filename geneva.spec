### RPM external geneva 1.0-RC3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Source: git+https://stash.desy.de/scm/geneva/geneva-public.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
# no-cmssdt-cache=1 part is used to instruct cmsBuild to not cache these files.
# no-cmssdt-cache=1 is removed by cmsBuild
Source2: http://cmsrep.cern.ch/cmssw/download/%{n}/%{realversion}no-cmssdt-cache=1/CT10nnlo_beamfunc.tar.gz
Source3: http://cmsrep.cern.ch/cmssw/download/%{n}/%{realversion}no-cmssdt-cache=1/MMHT2014nnlo68cl_beamfunc.tar.gz
Source4: http://cmsrep.cern.ch/cmssw/download/%{n}/%{realversion}no-cmssdt-cache=1/NNPDF31_nnlo_as_0118_beamfunc.tar.gz
Source5: http://cmsrep.cern.ch/cmssw/download/%{n}/%{realversion}no-cmssdt-cache=1/PDF4LHC15_nnlo_100_beamfunc.tar.gz

BuildRequires: cmake gmake

Requires: python py2-setuptools py2-numpy gsl OpenBLAS lhapdf hepmc pythia8
%ifnarch ppc64le
Requires: openloops
%endif

%prep
%setup -q -n %{n}-%{realversion}
mkdir -p share/Geneva/beamfunc
cp %{_sourcedir}/*_beamfunc.tar.gz share/Geneva/beamfunc

%build

%ifnarch ppc64le
export OPENLOOPS_FLAG="-Dopenloops_ROOT=${OPENLOOPS_ROOT}"
%endif

export LDFLAGS="-L${OPENBLAS_ROOT}/lib -lopenblas"
sed -i -e 's|OPTIONAL_COMPONENTS  *gslcblas||' cmake/configure-packages.cmake
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
      -DCMAKE_INSTALL_PREFIX=%{i} \
      -DCMAKE_CXX_STANDARD=11 \
      -Dgsl_ROOT=${GSL_ROOT} \
      -Dlhapdf_ROOT=${LHAPDF_ROOT} \
      -Dhepmc_ROOT=${HEPMC_ROOT} \
      -Dpythia8_ROOT=${PYTHIA8_ROOT} ${OPENLOOPS_FLAG}

make %{makeprocesses}
make beamfunc-install-data LHAPDF_DATA_PATH=${LHAPDF_ROOT}/share/LHAPDF

%install
cd ../build
make install
sed -i '/#!/c\#!/usr/bin/env python' %{i}/bin/*
