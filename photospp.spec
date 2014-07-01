### RPM external photospp 3.55

Requires: hepmc

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/photos++/photos++-%{realversion}-src.tgz

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -g -O2
%endif

%define keep_archives true

%prep
%setup -q -n photos++/%{realversion}

case %cmsplatf in
  osx*)
  ;;
esac

export HEPMCLOCATION=${HEPMC_ROOT}
export HEPMCVERSION=${HEPMC_VERSION}

./configure --prefix=%{i} --with-hepmc=$HEPMC_ROOT CXXFLAGS="%cms_cxxflags"
# One more fix-up for OSX (in addition to the patch above)
case %cmsplatf in
  osx*)
perl -p -i -e "s|-shared|-dynamiclib -undefined dynamic_lookup|" make.inc
  ;;
esac

%build
make %makeprocesses

%install
make install
ls %{i}/lib/

