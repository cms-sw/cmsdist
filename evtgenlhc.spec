### RPM external evtgenlhc 9.1
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: evtgenlhc-8.16-EvtPythia-iosfwd
Patch1: evtgenlhc-9.1-gcc43
Patch2: evtgenlhc-9.1-CLHEP2
Patch3: evtgenlhc-9.1-macosx
Patch4: evtgenlhc-9.1-fixPythiaDecay
Requires: clhep
Requires: pythia6
Requires: photos

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2
%patch2 -p2
%patch3 -p3
%patch4 -p2

%build
./configure --lcgplatform=%cmsplatf --with-clhep=$CLHEP_ROOT
# The configure script does not actually specifies the -L$CLHEP_ROOT & co. 
# On macosx this is fatal, We work around the problem by patching the makefile
# and by setting the needed link time dependencies by hand.
make PYTHIA6_ROOT=$PYTHIA6_ROOT CLHEP_ROOT=$CLHEP_ROOT PHOTOS_ROOT=$PHOTOS_ROOT

%install
tar -c lib EvtGen EvtGenBase EvtGenModels DecFiles | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="evtgenlhc" version="%v">
    <lib name="evtgenlhc"/>
    <client>
      <environment name="EVTGENLHC_BASE" default="%i"/>
      <environment name="LIBDIR" default="$EVTGENLHC_BASE/lib"/>
      <environment name="INCLUDE" default="$EVTGENLHC_BASE"/>
    </client>
    <use name="clhep"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
