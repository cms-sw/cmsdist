### RPM external pythia6 424
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz

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
./configure --enable-shared --with-hepevt=4000 

%build
make 
make install

%install
tar -c lib include | tar -x -C %i
