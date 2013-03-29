### RPM external herwig 6.520
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: lhapdf photos 
Patch1: herwig-6.520-tauoladummy

%define keep_archives true

%prep
%setup -q -n %n/%{realversion}
case %cmsplatf in
  slc5_*_gcc4[01234]*)
    F77="`which gfortran`"
    PLATF_CONFIG_OPTS="--enable-shared"
  ;;
  *)
    F77="`which gfortran` -fPIC"
    PLATF_CONFIG_OPTS="--disable-shared --enable-static"
  ;;
esac

%patch1 -p2

./configure $PLATF_CONFIG_OPTS --prefix=%i F77="$F77"

%build
make %{makeprocesses} LHAPDF_ROOT=$LHAPDF_ROOT PHOTOS_ROOT=$PHOTOS_ROOT

make check

%install
make install

# then hack include area as jimmy depends on missing header file..
# but only on slc*. On macosx HERWIG65.INC == herwig65.inc
# what is actually needed is a link to herwig6510.inc
%ifos darwin
ln -sf herwig6520.inc %{i}/include/herwig65.inc
%else
ln -sf HERWIG65.INC %{i}/include/herwig65.inc
%endif

rm -rf %i/lib/*.la
