### RPM external pythia8 135
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Requires: hepmc
Requires: clhep
Requires: pythia6
Requires: lhapdf

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}

export PYTHIA6LOCATION=${PYTHIA6_ROOT} 
export PYTHIA6VERSION=${PYTHIA6_VERSION} 
export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
export CLHEPLOCATION=${CLHEP_ROOT} 
export CLHEPVERSION=${CLHEP_VERSION}
./configure --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
tar -c lib include xmldoc | tar -x -C %i

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="pythia8" version="%v">
    <lib name="pythia8"/>
    <lib name="hepmcinterface"/>
    <client>
      <environment name="PYTHIA8_BASE" default="%i"/>
      <environment name="LIBDIR" default="$PYTHIA8_BASE/lib"/>
      <environment name="INCLUDE" default="$PYTHIA8_BASE/include"/>
    </client>
    <runtime name="PYTHIA8DATA" value="$PYTHIA8_BASE/xmldoc"/>
    <use name="cxxcompiler"/>
    <use name="hepmc"/>
    <use name="pythia6"/>
    <use name="clhep"/>
    <use name="lhapdf"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
