### RPM external pythia6 422
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: pythia6.422-writesyntax 

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

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
%patch0 -p2
./configure --enable-shared --with-hepevt=4000 

%build
make 
make install

%install
tar -c lib include | tar -x -C %i
