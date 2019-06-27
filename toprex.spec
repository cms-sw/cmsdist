### RPM external toprex 4.23

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch1: toprex-4.23-macosx
Patch2: toprex-4.23-archive-only
Requires: pythia6

%define keep_archives true

%prep
%setup -q -n %{n}/%{realversion}
# Remove options by hand since it looks like they have
# the bad habit of republishing sources.
perl -p -i -e 's|-fno-globals||g;s|-finit-local-zero||g;s|-fugly-logint||g' configure

%patch1 -p3
%patch2 -p3

%build
FC="$(which gfortran) -fPIC"

./configure --lcgplatform=%cmsplatf
make FC="$FC" PYTHIA6_ROOT=$PYTHIA6_ROOT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive
# bla bla
