### RPM external toprex 4.23

Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/toprex/%{n}-%{realversion}-src.tgz
Patch1: toprex-4.23-macosx
Patch2: toprex-4.23-archive-only
Requires: pythia6

%define keep_archives true

%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
# Remove options by hand since it looks like they have
# the bad habit of republishing sources.
perl -p -i -e 's|-fno-globals||g;s|-finit-local-zero||g;s|-fugly-logint||g' configure

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
