### RPM external evtgen 1.6.0

Requires: hepmc
Requires: pythia8
Requires: tauolapp
Requires: photospp

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

# See https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40267
# libgfortranbegin.a is finally removed and was obsolete since GCC 4.5
Patch0: evtgen-1.6.0-configure-new-gcc

%define keep_archives true

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2

case %cmsplatf in
  osx*)
  ;;
esac

./configure --prefix=%{i} --hepmcdir=$HEPMC_ROOT --pythiadir=$PYTHIA8_ROOT --tauoladir=$TAUOLAPP_ROOT --photosdir=$PHOTOSPP_ROOT

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
