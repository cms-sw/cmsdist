### RPM external sherpa-toolfile 1.0
Requires: sherpa
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/sherpa.xml
<tool name="sherpa" version="@TOOL_VERSION@">
<lib name="AhadicDecays"/>
<lib name="AhadicFormation"/>
<lib name="AhadicMain"/>
<lib name="AhadicTools"/>
<lib name="AmegicCluster"/>
<lib name="AmegicPSGen"/>
<lib name="Amegic"/>
<lib name="AmisicModel"/>
<lib name="Amisic"/>
<lib name="AmisicTools"/>
<lib name="Amplitude"/>
<lib name="Beam"/>
<lib name="ComixAmplitude"/>
<lib name="ComixCluster"/>
<lib name="ComixPhasespace"/>
<lib name="Comix"/>
<lib name="CSCalculators"/>
<lib name="CSMain"/>
<lib name="CSShowers"/>
<lib name="CSTools"/>
<lib name="CT10Sherpa"/>
<lib name="CT12Sherpa"/>
<lib name="CTEQ6Sherpa"/>
<lib name="DipoleSubtraction"/>
<lib name="ExtraXS1_2"/>
<lib name="ExtraXS1_3"/>
<lib name="ExtraXS2_2"/>
<lib name="ExtraXSCluster"/>
<lib name="ExtraXSNLO"/>
<lib name="ExtraXS"/>
<lib name="GRVSherpa"/>
<lib name="HadronsCurrents"/>
<lib name="HadronsMain"/>
<lib name="HadronsMEs"/>
<lib name="HadronsPSs"/>
<lib name="LHAPDFSherpa"/>
<lib name="LundTools"/>
<lib name="MCatNLOCalculators"/>
<lib name="MCatNLOMain"/>
<lib name="MCatNLOShowers"/>
<lib name="MCatNLOTools"/>
<lib name="MEProcess"/>
<lib name="METoolsColors"/>
<lib name="METoolsCurrents"/>
<lib name="METoolsExplicit"/>
<lib name="METoolsLoops"/>
<lib name="METoolsMain"/>
<lib name="METoolsSpinCorrelations"/>
<lib name="METoolsVertices"/>
<lib name="ModelInteractions"/>
<lib name="ModelMain"/>
<lib name="MRST01LOSherpa"/>
<lib name="MRST04QEDSherpa"/>
<lib name="MRST99Sherpa"/>
<lib name="MSTW08Sherpa"/>
<lib name="PDFESherpa"/>
<lib name="PDF"/>
<lib name="PhasicChannels"/>
<lib name="PhasicDecays"/>
<lib name="PhasicEnhance"/>
<lib name="PhasicMain"/>
<lib name="PhasicProcess"/>
<lib name="PhasicScales"/>
<lib name="PhasicSelectors"/>
<lib name="PhotonsMain"/>
<lib name="PhotonsMEs"/>
<lib name="PhotonsPhaseSpace"/>
<lib name="PhotonsTools"/>
<lib name="Remnant"/>
<lib name="SherpaAnalyses"/>
<lib name="SherpaAnalysis"/>
<lib name="SherpaAnalysisTools"/>
<lib name="SherpaAnalysisTrigger"/>
<lib name="SherpaBlackHat"/>
<lib name="SherpaHepMCOutput"/>
<lib name="SherpaHiggs"/>
<lib name="SherpaInitialization"/>
<lib name="SherpaMain"/>
<lib name="SherpaObservables"/>
<lib name="SherpaPythia"/>
<lib name="SherpaPerturbativePhysics"/>
<lib name="SherpaSingleEvents"/>
<lib name="SherpaSoftPhysics"/>
<lib name="SherpaTools"/>
<lib name="ShrimpsBeamRemnants"/>
<lib name="ShrimpsEikonals"/>
<lib name="ShrimpsEvents"/>
<lib name="ShrimpsMain"/>
<lib name="ShrimpsTools"/>
<lib name="ShrimpsXsecs"/>
<lib name="String"/>
<lib name="ToolsMath"/>
<lib name="ToolsOrg"/>
<lib name="ToolsPhys"/>
<lib name="Zfunctions"/>
<client>
<environment name="SHERPA_BASE" default="@TOOL_ROOT@"/>
<environment name="BINDIR" default="$SHERPA_BASE/bin"/>
<environment name="LIBDIR" default="$SHERPA_BASE/lib/SHERPA-MC"/>
<environment name="INCLUDE" default="$SHERPA_BASE/include/SHERPA-MC"/>
</client>
<runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$SHERPA_BASE/include" type="path"/>
<runtime name="SHERPA_SHARE_PATH" value="$SHERPA_BASE/share/SHERPA-MC" type="path"/>
<runtime name="SHERPA_INCLUDE_PATH" value="$SHERPA_BASE/include/SHERPA-MC" type="path"/>
<use name="HepMC"/>
<use name="lhapdf"/>
<use name="qd"/>
<use name="blackhat"/>
<use name="fastjet"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
