### RPM external toprex 4.23

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: toprex-4.23-gfortran
Patch1: toprex-4.23-macosx
Patch2: toprex-4.23-archive-only
Requires: pythia6

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p0 
%patch1 -p3
case %cmsos in
  osx*)
%patch2 -p3
  ;;
esac

%build
./configure --lcgplatform=%cmsplatf
make FC="`which gfortran` -fPIC" PYTHIA6_ROOT=$PYTHIA6_ROOT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive
