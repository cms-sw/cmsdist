### RPM external herwig 6.520
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: lhapdf photos tauola
Patch1: herwig-6.520-tauoladummy

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

./configure --enable-shared --prefix=%i F77=gfortran

%build
make %{makeprocesses} TAUOLA_ROOT=$TAUOLA_ROOT LHAPDF_ROOT=$LHAPDF_ROOT PHOTOS_ROOT=$PHOTOS_ROOT

make check

%install
make install

# then hack include area as jimmy depends on missing header file..
# but only on slc*. On macosx HERWIG65.INC == herwig65.inc
# what is actually needed is a link to herwig6510.inc
cd %i/include
case %cmsplatf in
    slc*)
	ln -sf HERWIG65.INC herwig65.inc
    ;;
    osx*)
	ln -sf herwig6520.inc herwig65.inc
    ;;
esac
