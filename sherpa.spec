### RPM external sherpa 1.2.2
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

#Source: http://cern.ch/service-spi/external/MCGenerators/distribution/sherpa-%{realversion}-src.tgz
Source: http://www.hepforge.org/archive/sherpa/SHERPA-MC-%{realversion}.tar.gz

Requires: hepmc lhapdf

%prep
#%setup -n sherpa/%{realversion}
%setup -n SHERPA-MC-%{realversion}

autoreconf -i

# Assumes 32bit for non-amd64, may not be correct for all platforms
case %cmsos in
  slc*_amd64)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit"
   ;;
  slc*_ia32)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit -m32"
  ;;
  *)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit -m32"
esac


%build
case %gccver in
  3.*)
export FC=g77
  ;;
esac

# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
for file in `find ./ -name Makefile`; do
  perl -p -i -e 's|/usr/lib64/libm.a||' $file
  perl -p -i -e 's|/usr/lib64/libc.a||' $file
done

make

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
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
    <lib name="ComixCurrents"/>
    <lib name="ComixModels"/>
    <lib name="ComixPhasespace"/>
    <lib name="Comix"/>
    <lib name="ComixVertices"/>
    <lib name="CSCalculators"/>
    <lib name="CSMain"/>
    <lib name="CSShowers"/>
    <lib name="CSTools"/>
    <lib name="CTEQ6Sherpa"/>
    <lib name="DipoleSubtraction"/>
    <lib name="ExtraXS2_2"/>
    <lib name="ExtraXSCluster"/>
    <lib name="ExtraXSNLO"/>
    <lib name="ExtraXS"/>
    <lib name="GRVSherpa"/>
    <lib name="HadronsCurrents"/>
    <lib name="HadronsMain"/>
    <lib name="HadronsMEs"/>
    <lib name="HadronsPSs"/>
    <lib name="HelicitiesLoops"/>
    <lib name="HelicitiesMain"/>
    <lib name="LHAPDFSherpa"/>
    <lib name="LundTools"/>
    <lib name="ModelInteractions"/>
    <lib name="ModelMain"/>
    <lib name="MRST01LOSherpa"/>
    <lib name="MRST04QEDSherpa"/>
    <lib name="MRST99Sherpa"/>
    <lib name="MSTW08Sherpa"/>
    <lib name="PDFESherpa"/>
    <lib name="PDF"/>
    <lib name="PhasicChannels"/>
    <lib name="PhasicMain"/>
    <lib name="PhasicProcess"/>
    <lib name="PhasicScales"/>
    <lib name="PhasicSelectors"/>
    <lib name="PhotonsMain"/>
    <lib name="PhotonsMEs"/>
    <lib name="PhotonsPhaseSpace"/>
    <lib name="PhotonsTools"/>
    <lib name="Remnant"/>
    <lib name="SherpaAnalysis"/>
    <lib name="SherpaAnalysisTools"/>
    <lib name="SherpaAnalysisTrigger"/>
    <lib name="SherpaInitialization"/>
    <lib name="SherpaMain"/>
    <lib name="SherpaObservables"/>
    <lib name="SherpaPerturbativePhysics"/>
    <lib name="SherpaSingleEvents"/>
    <lib name="SherpaSoftPhysics"/>
    <lib name="SherpaTools"/>
    <lib name="String"/>
    <lib name="ToolsMath"/>
    <lib name="ToolsOrg"/>
    <lib name="ToolsPhys"/>
    <lib name="Zfunctions"/>
    <client>
      <environment name="SHERPA_BASE" default="%i"/>
      <environment name="BINDIR" default="$SHERPA_BASE/bin"/>
      <environment name="LIBDIR" default="$SHERPA_BASE/lib/SHERPA-MC"/>
      <environment name="INCLUDE" default="$SHERPA_BASE/include/SHERPA-MC"/>
    </client>
    <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$SHERPA_BASE/include" type="path"/>
    <runtime name="SHERPA_SHARE_PATH" value="$SHERPA_BASE/share/SHERPA-MC" type="path"/>
    <runtime name="SHERPA_INCLUDE_PATH" value="$SHERPA_BASE/include/SHERPA-MC" type="path"/>
    <use name="HepMC"/>
    <use name="lhapdf"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
