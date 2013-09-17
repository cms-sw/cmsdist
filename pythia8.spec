### RPM external pythia8 175 
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif

Requires: hepmc

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{n}/%{realversion}

export USRCXXFLAGS="%cms_cxxflags"
export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
case %{cmsplatf} in
   *_mic_* )
     CXX="icc" CC="icc" USRLDFLAGSSHARED="-fPIC -mmic" USRCXXFLAGS="-fPIC -mmic $USRCXXFLAGS" ./configure --enable-shared --with-hepmc=${HEPMC_ROOT}
     ;;
   * )
    ./configure --enable-shared --with-hepmc=${HEPMC_ROOT}
     ;;
esac

%build
make 

%install
tar -c lib include xmldoc | tar -x -C %i
