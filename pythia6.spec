### RPM external pythia6 422
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep

case %gccver in
  4.*)
export F77=gfortran
  ;;
  3.*)
export F77=g77
  ;;
esac

%setup -q -n %{n}/%{realversion}
./configure --enable-shared --with-hepevt=4000 

%build
make 
make install

%install
tar -c lib include | tar -x -C %i
