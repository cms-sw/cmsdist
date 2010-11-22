### RPM external cascade 2.2.0

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: cascade-2.2.0-nomanual
Requires: lhapdf pythia6
%prep

case %gccver in
 4.*)
export F77=gfortran
 ;;
esac

%setup -q -n %{n}/%{realversion}
%patch0 -p2

export PYTHIA="$PYTHIA6_ROOT"
export LHAPDF="$LHAPDF_ROOT"

./configure --enable-shared --with-hepevt=4000 --prefix=%i

%build
make 

%install
make install
