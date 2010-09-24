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
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="pythia6" version="%v">
    <lib name="pythia6"/>
    <lib name="pythia6_dummy"/>
    <lib name="pythia6_pdfdummy"/>
    <client>
      <environment name="PYTHIA6_BASE" default="%i"/>
      <environment name="LIBDIR" default="$PYTHIA6_BASE/lib"/>
      <environment name="INCLUDE" default="$PYTHIA6_BASE/include"/>
    </client>
    <use name="f77compiler"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
