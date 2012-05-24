### RPM external tauolapp 1.0.5
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++-%{realversion}-src.tgz
#Patch0: tauolapp-1.0.2a-osx-Makefile
Requires: hepmc

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n tauola++/%{realversion}

export HEPMCLOCATION=${HEPMC_ROOT}
export HEPMCVERSION=${HEPMC_VERSION}

case %cmsplatf in 
  osx*)
#%patch0 -p2
  ;;
esac

./configure --prefix=%{i} --with-hepmc=$HEPMC_ROOT
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

