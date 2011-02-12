### RPM external toprex 4.23

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: toprex-4.23-gfortran
Patch1: toprex-4.23-macosx
Requires: pythia6

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  4.*)
%patch0 -p0 
  ;; 
esac
%patch1 -p3

%build
./configure --lcgplatform=%cmsplatf
make  PYTHIA6_ROOT=$PYTHIA6_ROOT

%install
tar -c lib include | tar -x -C %i
