### RPM external cascade 2.2.0

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: cascade-2.2.0-nomanual
Requires: lhapdf pythia6
%prep

%setup -q -n %{n}/%{realversion}
%patch0 -p2

# Notice that cascade expects a flat pythia installation,
# where libraries and headers are all in the same place.
# Since the source code is not actually needed, we point
# it to the library location so that it links correctly.
PYTHIA="$PYTHIA6_ROOT/lib"
LHAPDF="$LHAPDF_ROOT"
case %cmsplatf in 
  slc5_*_gcc4[0123]*)
    F77="`which gfortran`"
    PLATF_CONFIG_OPTS="--enable-shared"
  ;;
  *)
    F77="`which gfortran` -fPIC"
    PLATF_CONFIG_OPTS="--enable-static --disable-shared"
    LIBS='-lstdc++ -lz'
  ;;
esac
PYTHIA=$PYTHIA LHAPDF=$LHAPDF ./configure $PLATF_CONFIG_OPTS --with-hepevt=4000 --prefix=%i F77="$F77" LIBS="$LIBS" 
%build
make %makeprocesses

%install
make install

