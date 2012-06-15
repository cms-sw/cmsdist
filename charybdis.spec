### RPM external charybdis 1.003
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: charybdis-1003-macosx

Requires: pythia6
Requires: lhapdf

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p3
./configure --lcgplatform=%cmsplatf --pythia_hadronization

%build
make PYTHIA6_ROOT=$PYTHIA6_ROOT LHAPDF_ROOT=$LHAPDF_ROOT

%install
tar -c lib include | tar -x -C %i
