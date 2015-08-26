### RPM external evtgen 1.4.0p1

Requires: hepmc
Requires: pythia8
Requires: tauolapp
Requires: photospp

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -g -O2
%endif

%define keep_archives true

%prep
%setup -q -n %{n}/%{realversion}

case %cmsplatf in
  osx*)
  ;;
esac

./configure --prefix=%{i} --hepmcdir=$HEPMC_ROOT --pythiadir=$PYTHIA8_ROOT --tauoladir=$TAUOLAPP_ROOT --photosdir=$PHOTOSPP_ROOT CXXFLAGS="%cms_cxxflags" 

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
