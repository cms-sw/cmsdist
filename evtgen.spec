### RPM external evtgen 1.3.0

Requires: hepmc
Requires: pythia8
Requires: tauolapp
Requires: photospp

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/evtgen/evtgen-1.3.0-src.tgz

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -g -O2
%endif

%define keep_archives true

%prep
%setup -q -n evtgen/%{realversion}

case %cmsplatf in
  osx*)
  ;;
esac

export HEPMCLOCATION=${HEPMC_ROOT}
export HEPMCVERSION=${HEPMC_VERSION}
export PYTHIA8_LOCATION=${PYTHIA8_ROOT}
export TAUOLAPP_LOCATION=${TAUOLAPP_ROOT}
export PHOTOSPP_LOCATION=${PHOTOSPP_ROOT}


./configure --prefix=%{i} --hepmcdir=$HEPMC_ROOT --pythiadir=$PYTHIA8_ROOT --tauoladir=$TAUOLAPP_ROOT --photosdir=$PHOTOSPP_ROOT CXXFLAGS="%cms_cxxflags" 
#remove obsolete pythia8 library
sed -i 's/PYTHIALIBLIST = -lpythia8 -llhapdfdummy/PYTHIALIBLIST = -lpythia8/g' config.mk

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
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive
ls %{i}/lib/

