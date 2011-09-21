### RPM external evtgenlhc 9.1
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz?date=20110831
Patch0: evtgenlhc-8.16-EvtPythia-iosfwd
Patch1: evtgenlhc-9.1-gcc43
Patch2: evtgenlhc-9.1-CLHEP2
Patch3: evtgenlhc-9.1-macosx
Patch4: evtgenlhc-9.1-fixPythiaDecay
Patch5: evtgenlhc-9.1-gcc46
Requires: clhep
Requires: pythia6
Requires: photos
%define keep_archives true

%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2
%patch2 -p2
%patch3 -p3
%patch4 -p2
%patch5 -p2

%build
# On old architectures we build dynamic libraries, on 
# new ones archives.
case %cmsos in
  slc5_*_gcc4[01234]*) ;;
  *) BUILD_PRODUCT=lib_archive ;;
esac
./configure --lcgplatform=%cmsplatf --with-clhep=$CLHEP_ROOT
# The configure script does not actually specifies the -L$CLHEP_ROOT & co. 
# On macosx this is fatal, We work around the problem by patching the makefile
# and by setting the needed link time dependencies by hand.
make PYTHIA6_ROOT=$PYTHIA6_ROOT CLHEP_ROOT=$CLHEP_ROOT PHOTOS_ROOT=$PHOTOS_ROOT $BUILD_PRODUCT

%install
tar -c lib EvtGen EvtGenBase EvtGenModels DecFiles | tar -x -C %i
mv %i/lib/archive/*.a %i/lib
rm -rf %i/lib/archive
