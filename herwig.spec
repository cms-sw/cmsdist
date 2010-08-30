### RPM external herwig 6.510.3
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: lhapdf photos tauola
Patch1: herwig-6.510-tauola
Patch2: herwig-6.510.3-nmxhep
Patch3: herwig-6.510.3-macosx

%prep
%setup -q -n %n/%{realversion}
# Danger - herwig doesn't actually need the hepmc, clhep,lhapdf 
# that appear to be used in the configure

# move tauola/photos dummy functions in new directory
mkdir tauoladummy
mv ./dummy/dexay.f ./tauoladummy/ 
mv ./dummy/inietc.f ./tauoladummy/ 
mv ./dummy/inimas.f ./tauoladummy/ 
mv ./dummy/iniphx.f ./tauoladummy/ 
mv ./dummy/initdk.f ./tauoladummy/ 
mv ./dummy/phoini.f ./tauoladummy/ 
mv ./dummy/photos.f ./tauoladummy/ 

# apply patch to modify Makefile
%patch1 -p2
%patch2 -p2
%patch3 -p3

# move the rest of the dummy files in the src directory, so that they get picked up.
cp dummy/*.f src

./configure --enable-shared

%build
#perl -p -i -e 's|libherwig([^.]).so|libherwig$1.dylib|g' Makefile
make TAUOLA_ROOT=$TAUOLA_ROOT LHAPDF_ROOT=$LHAPDF_ROOT PHOTOS_ROOT=$PHOTOS_ROOT

# then hack include area as jimmy depends on missing header file..
# but only on slc*. On macosx HERWIG65.INC == herwig65.inc
# what is actually needed is a link to herwig6510.inc
cd include
case %cmsplatf in
    slc*)
	ln -sf HERWIG65.INC herwig65.inc
    ;;
    osx*)
	ln -sf herwig6510.inc herwig65.inc
    ;;
esac

%install
tar -c lib include | tar -x -C %i
