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
case %cmsplatf in
  slc5_*_gcc4[01234]*) ;;
  *) 
%patch2 -p3
  ;;
esac
%build
# NOTE: old platforms were built using dynamic libraries. Since
#       gcc451 or on mac we need to use archive ones (because of gold).
case %cmsplatf in
  slc5_*_gcc4[01234]*) FC="`which gfortran`" ;;
  *) FC="`which gfortran` -fPIC" ;;
esac

./configure --lcgplatform=%cmsplatf
make FC="$FC" PYTHIA6_ROOT=$PYTHIA6_ROOT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

