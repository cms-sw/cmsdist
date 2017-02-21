### RPM external tauolapp 1.1.5
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-%{realversion}-src.tgz
Requires: hepmc
Requires: pythia8
Requires: lhapdf

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -g -O2
%endif

%define keep_archives true

%prep
%setup -q -n tauola++/%{realversion}

export HEPMCLOCATION=${HEPMC_ROOT}
export HEPMCVERSION=${HEPMC_VERSION}
export LHAPDF_LOCATION=${LHAPDF_ROOT}
export PYTHIA8_LOCATION=${PYTHIA8_ROOT}

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

./configure --prefix=%{i} --with-hepmc=$HEPMC_ROOT --with-pythia8=$PYTHIA8_ROOT --with-lhapdf=$LHAPDF_ROOT CXX="%cms_cxx" CPPFLAGS="%cms_cxxflags -I${BOOST_ROOT}/include"

%ifos darwin
perl -p -i -e "s|-shared|-dynamiclib -undefined dynamic_lookup|" make.inc
%endif

%build
make

%install
make install

mkdir %{i}/share
cp TauSpinner/examples/CP-tests/Z-pi/*.txt %{i}/share/
