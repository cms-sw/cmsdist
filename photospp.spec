### RPM external photospp 3.61

Requires: hepmc

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/photos++/photos++-%{realversion}-src.tgz

%define keep_archives true

%prep
%setup -q -n photos++/%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

export HEPMCLOCATION=${HEPMC_ROOT}
export HEPMCVERSION=${HEPMC_VERSION}

./configure --prefix=%{i} --with-hepmc=${HEPMC_ROOT}

%ifos darwin
perl -p -i -e "s|-shared|-dynamiclib -undefined dynamic_lookup|" make.inc
%endif

%build
make %{makeprocesses}

%install
make install
ls %{i}/lib/
