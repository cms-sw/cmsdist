### RPM external herwig 6.520
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: lhapdf photos 
Patch1: herwig-6.520-tauoladummy

%prep
%setup -q -n %n/%{realversion}

./configure --enable-shared --prefix=%i F77=gfortran

%build
make %{makeprocesses} LHAPDF_ROOT=$LHAPDF_ROOT PHOTOS_ROOT=$PHOTOS_ROOT

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
