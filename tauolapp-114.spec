### RPM external tauolapp 1.1.4

Requires: hepmc
Requires: pythia8
Requires: lhapdf

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-%{realversion}-src.tgz

Patch0: tauolapp_114-patchhook

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -g -O2
%endif

%define keep_archives true

%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n tauola++/%{realversion}
%patch0 -p1

case %cmsplatf in 
  osx*)
  ;;
esac

export HEPMCLOCATION=${HEPMC_ROOT}
export HEPMCVERSION=${HEPMC_VERSION}
export LHAPDF_LOCATION=${LHAPDF_ROOT}
export PYTHIA8_LOCATION=${PYTHIA8_ROOT}

./configure --prefix=%{i} --with-hepmc=$HEPMC_ROOT --with-pythia8libs=$PYTHIA_ROOT --with-lhapdf=$LHAPDF_ROOT CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags"
# One more fix-up for OSX (in addition to the patch above)
case %cmsplatf in
  osx*)
perl -p -i -e "s|-shared|-dynamiclib -undefined dynamic_lookup|" make.inc
  ;;
esac

%build
make

%install
make install
