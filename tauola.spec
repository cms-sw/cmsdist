### RPM external tauola 27.121.5
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch: tauola-27.121-gfortran
Patch1: tauola-27.121.5-gfortran-taueta
Patch2: tauola-27.121-gfortran-tauola-srs
Patch3: tauola-27.121.5-macosx
Requires: pythia6
Requires: photos

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  4.*)
%patch -p0 
%patch1 -p2
%patch2 -p2
  ;;
esac
%patch3 -p3
./configure --lcgplatform=%cmsplatf --with-pythia6libs=$PYTHIA6_ROOT/lib

%build
case %cmsplatf in 
  osx*)
  perl -p -i -e 's|libtauola.so|libtauola.dylib|g' Makefile
  perl -p -i -e 's|libpretauola.so|libpretauola.dylib|g' Makefile
  ;;
esac
make PHOTOS_ROOT=$PHOTOS_ROOT

%install
tar -c lib include | tar -x -C %i
