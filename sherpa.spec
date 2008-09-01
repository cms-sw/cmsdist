### RPM external sherpa 1.1.2
Source: http://www.hepforge.org/archive/sherpa/Sherpa-%realversion.tar.gz

Requires: hepmc lhapdf

Patch: sherpa-lhapdf

%prep
%setup -n SHERPA-MC-%realversion
%patch -p1

%build
# in case of errors the tool prompts ... and the build process hangs forever :(
echo "a" | ./TOOLS/makeinstall -t --copt --enable-hepmc2=$HEPMC_ROOT --copt --enable-lhapdf=$LHAPDF_ROOT --copt --prefix=%i

%install
#make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
    <lib name="SherpaMain"/>
    <lib name="AhadicDecays"/>
    <lib name="AhadicFormation"/>
    <lib name="AhadicMain"/>
    <lib name="AhadicTools"/>
    <lib name="AmegicPSGen"/>
    <lib name="Amegic"/>
    <lib name="AmisicModel"/>
    <lib name="Amisic"/>
    <lib name="AmisicTools"/>
    <lib name="Amplitude"/>
    <lib name="AnalysisDetector"/>
    <lib name="Analysis"/>
    <lib name="AnalysisTools"/>
    <lib name="AnalysisTriggers"/>
    <lib name="ApacicMain"/>
    <lib name="ApacicShowers"/>
    <lib name="Beam"/>
    <lib name="ExtraXS2_2"/>
    <lib name="ExtraXSModel"/>
    <lib name="ExtraXS"/>
    <lib name="GRV"/>
    <lib name="HadronsCurrents"/>
    <lib name="HadronsMain"/>
    <lib name="HadronsMEs"/>
    <lib name="HadronsPSs"/>
    <lib name="HelicitiesMain"/>
    <lib name="LHAPDFSherpa"/>
    <lib name="LundTools"/>
    <lib name="ModelDecays"/>
    <lib name="ModelInteractions"/>
    <lib name="ModelMain"/>
    <lib name="Observables"/>
    <lib name="PDF"/>
    <lib name="Phasespace"/>
    <lib name="PhotonsMain"/>
    <lib name="PhotonsMEs"/>
    <lib name="PhotonsPhaseSpace"/>
    <lib name="PhotonsTools"/>
    <lib name="Remnant"/>
    <lib name="SherpaInitialization"/>
    <lib name="SherpaPerturbativePhysics"/>
    <lib name="SherpaSingleEvents"/>
    <lib name="SherpaSoftPhysics"/>
    <lib name="SherpaTools"/>
    <lib name="String"/>
    <lib name="Sudakov"/>
    <lib name="ToolsMath"/>
    <lib name="ToolsOrg"/>
    <lib name="ToolsPhys"/>
    <lib name="Zfunctions"/>
    <client>
      <Environment name="SHERPA_BASE" default="%i"/>
      <Environment name="BINDIR" default="$SHERPA_BASE/bin"/>
      <Environment name="LIBDIR" default="$SHERPA_BASE/lib/SHERPA-MC"/>
      <Environment name="INCLUDE" default="$SHERPA_BASE/include"/>
    </client>
    <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$SHERPA_BASE/include" type="path"/>
    <use name="HepMC"/>
    <use name="lhapdf"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
