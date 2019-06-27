### RPM external charybdis 1.003
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: charybdis-1003-macosx
Patch1: charybdis-1.003-archive-only

Requires: pythia6
Requires: lhapdf
Requires: zlib

%define keep_archives true

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p3
# On osx we build only the archive libraries to avoid issues with the common
# blocks.
case %cmsos in
  osx*)
%patch1 -p3
  ;;
esac
./configure --lcgplatform=%cmsplatf --pythia_hadronization

%build
make FC="`which gfortran` -fPIC" PYTHIA6_ROOT=$PYTHIA6_ROOT LHAPDF_ROOT=$LHAPDF_ROOT ZLIB_ROOT=$ZLIB_ROOT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

# bla bla
