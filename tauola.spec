### RPM external tauola 27.121.5
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz?date=20110831
Patch1: tauola-27.121.5-gfortran-taueta
Patch2: tauola-27.121-gfortran-tauola-srs
Patch3: tauola-27.121.5-macosx
Patch4: tauola-27.121.5-archive-only
# Notice that on macosx we don't build shared libraries, so the following
# requires are not really mandatory, but we keep them for consistency with the
# linux build.
Requires: pythia6
Requires: photos

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
# Remove options by hand since it looks like they have
# the bad habit of republishing sources.
perl -p -i -e 's|-fno-globals||g;s|-finit-local-zero||g;s|-fugly-logint||g;s|-fugly-complex||' configure
# Removed since this appears to have already been applied in the new tarball...
# Sigh...
%patch1 -p2
%patch2 -p2
%patch3 -p3
# Build static library only on new platforms.
case %cmsplatf in 
  slc5_*_gcc4[01234]*) FC="`which gfortran`" ;;
  *) FC="`which gfortran` -fPIC" 
%patch4 -p3
  ;;
esac
./configure --lcgplatform=%cmsplatf --with-pythia6libs=$PYTHIA6_ROOT/lib FC="$FC"
case %cmsplatf in
  slc5_*_gcc4[01234]*) ;;
  *)
    # Make sure we compile with -fPIC also in the case of archive libraries.
    perl -p -i -e "s|FC = gfortran|FC = `which gfortran` -fPIC|;s|CC = gcc|CC = `which gcc` -fPIC|" config.mk
  ;;
esac
%build
make PHOTOS_ROOT=$PHOTOS_ROOT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

