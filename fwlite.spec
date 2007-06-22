### RPM cms fwlite CMSSW_1_5_0_FWLITE
## IMPORT configurations 
Provides: /bin/zsh
Requires: SCRAMV1
Requires: fwlite-tool-conf
Requires: gcc-wrapper
%define gccwrapperarch  slc4_ia32_gcc345 

# Take source from CMSSW base release:
%define application  %n
# Assuming release name convention for FWLite release based on CMSSW_X_Y_Z is CMSSW_X_Y_Z_FWLITE .
%define cmssw_release %(perl -e '$_="%v"; s/_FWLITE//; print;')
%define cmsswsrc           http://cmsdoc.cern.ch/cms/cpt/Software/download/cms/SOURCES/cms/cmssw/%{cmssw_release}
Source0: %{cmsswsrc}/toolbox.tar.gz
Source1: %{cmsswsrc}/config.tar.gz
Source2: %{cmsswsrc}/src.tar.gz

%define toolconf        ${FWLITE_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define prebuildtarget  gindices
%define buildtarget     release-build
%define postbuildtarget doc

# Following dependencies were not detected by ignominy, but required in the BuildFiles:
# boost_program_options boost_regex bz2lib pcre root rootcintex uuid zlib

%define externals "cxxcompiler ccompiler clhep sockets boost boost_filesystem rootrflx rootcore rootmath gccxml boost_python elementtree sigcpp hepmc gsl boost_regex boost_program_options boost_program_options boost_regex bz2lib pcre root rootcintex zlib"

%define packages "CondFormats/JetMETObjects DataFormats/BTauReco DataFormats/CLHEP DataFormats/CaloRecHit DataFormats/CaloTowers DataFormats/Candidate DataFormats/Common DataFormats/DetId DataFormats/EcalDetId DataFormats/EcalRecHit DataFormats/EgammaCandidates DataFormats/EgammaReco DataFormats/EgammaTrackReco DataFormats/FEDRawData DataFormats/GeometryCommonDetAlgo DataFormats/GeometrySurface DataFormats/GeometryVector DataFormats/GsfTrackReco DataFormats/HcalDetId DataFormats/HcalRecHit DataFormats/HepMCCandidate DataFormats/JetReco DataFormats/L1CaloTrigger DataFormats/L1GlobalCaloTrigger DataFormats/L1GlobalMuonTrigger DataFormats/L1Trigger DataFormats/METReco DataFormats/Math DataFormats/MuonDetId DataFormats/MuonReco DataFormats/ParticleFlowCandidate DataFormats/ParticleFlowReco DataFormats/Provenance DataFormats/RecoCandidate DataFormats/SiPixelCluster DataFormats/SiPixelDetId DataFormats/SiPixelDigi DataFormats/SiStripCluster DataFormats/SiStripCommon DataFormats/SiStripDetId DataFormats/SiStripDigi DataFormats/TrackCandidate DataFormats/TrackReco DataFormats/TrackerRecHit2D DataFormats/TrackingRecHit DataFormats/TrajectorySeed DataFormats/TrajectoryState DataFormats/VertexReco FWCore/FWLite FWCore/MessageLogger FWCore/PluginManager FWCore/RootAutoLibraryLoader FWCore/Utilities SimDataFormats/HepMCProduct"

%prep

# Create a SCRAM project area, but using the already extracted
# sources.  In other words, pick up the files from the project config
# area, but munge all instances of <base url="cvs:*"> into a local
# reference so SCRAM won't try to download stuff from the network.

%setup -T -b 0 -n SCRAMToolBox
%setup -D -T -b 1 -n config
%setup -D -T -b 2 -n src


# Update requirements:

%if "%{buildarch:set}" != "set"
%define buildarch	:
%endif

# NR: Allow to define bootstrap and requirements file names
%define bootstrapfile config/%{application}_bootsrc
%define reqfile config/%{application}_requirements


cd %_builddir

# Create bootstrap file for fwlite:
cp config/bootsrc %bootstrapfile
perl -p -i -e ' 
# s!(<project.*name=)CMSSW(.*version=)CMSSW(.*)!$1%projectname$2%projectname$3!;
 s!(<project.*name=CMSSW.*version=)%cmssw_release(.*)!$1%v$2!;
 s!config/requirements!%{reqfile}!;
 if (s/(<download.*)(module=)CMSSW(.*)(name="src)(">)/#$1$2$3$4$5/) {
   foreach $p (split / /, %{packages}) {
      print "$1$2src/$p$3$4/$p$5\n"
   }
  }
' %bootstrapfile

# Create requirements file:
cp config/requirements %reqfile
perl -p -i -e '
  if (m/(<select name=)(.*)(>)/) {
    foreach $t (split / /, %externals) {
      if ( $t eq lc($2) ) { $matches=1; last; }
    }
    if ( $matches != 1 ) { s/(.*)$/#$1/ }; 
    $matches=0;
  }
' %reqfile

# Create build templates: 
# for file in config/CMSSW_*.tmpl; do cat $file > `echo $file | sed s'/CMSSW/%{projectname}/'`; done

# Switch off building tests: 
perl -p -i -e ' s!(<ClassPath.*test\+test>)!#$1!;' config/BuildFile

# Munging algorithm from scramv1-build.file:
perl -p -i -e '
  # Keep track whether we are in a toolbox area or not
  if ($. == 1) { $intbx = 1; }
  if (/<base/) { $intbx = /SPITOOLS|SCRAMToolBox|scramtoolbox/; }

  # Replace base locations
  s!cvs://.*/(SPITOOLS|SCRAMToolBox|scramtoolbox)\?[^">]+!file:%_builddir/SCRAMToolBox/!;
  s!cvs://.*/(CMSSW)\?[^">]+!file:%_builddir/!;
  
  # Replace relative references depending on whether this is in
  # toolbox, or for project itself; configuration is always in
  # toolbox.  In toolbox keep cvs module name but drop the leading
  # SCRAMToolBox if there is one.  In project always replace with
  # rewritten paths.  (FIXME: produce source archive in cvs order?)
  if ($intbx) {
    s!url="cvs:\?module="?([^">]+)"?\s+name="?([^">]+)"?>!url="file:$1" name="$2">!;
    s!url="(cvs:\?module=|file:)SCRAMToolBox/(.*)">!url="file:$2">!;
    s!url="(cvs:\?module=|file:)scramtoolbox/(.*)">!url="file:$2">!;
  } else {
    #s!url="cvs:\?module="?([^">]+)"?\s+name="?([^">]+)"?>!url="file:$2" name="$2">!;
    s!<download\s+url="cvs:\?module=LCGAAwrappers/%cvsproj/[^"]+?"\s+name=.+>!!;
    s!url="cvs:\?module="?%cvssrc/([^">]+)"?\s+name="?([^">]+)"?>!url="file:src/$1" name="$2">!;
    s!url="cvs:\?module="?([^">]+)"?\s+name="?([^">]+)"?>!url="file:$1" name="$2">!;
  }
 ' %{bootstrapfile} \
   %{reqfile} \
   SCRAMToolBox/CMS/Configuration/CMSconfiguration

# Handle toolbox
pwd 
perl -p -i -e '
    # Replace base locations
    s!cvs://.*/(SPITOOLS|SCRAMToolBox)\?[^">]+!file:%_builddir/SCRAMToolBox/!;
    s!cvs://.*/(SPITOOLS|scramtoolbox)\?[^">]+!file:%_builddir/SCRAMToolBox/!;
    s!cvs://.*/%cvsdir\?[^">]+!file:%_builddir/!;
    s!url="cvs:\?module="?([^">]+)"?\s+name="?([^">]+)"?>!url="file:$1" name="$2">!;
    s!url="(cvs:\?module=|file:)SCRAMToolBox/(.*)">!url="file:$2">!;
    s!url="(cvs:\?module=|file:)scramtoolbox/(.*)">!url="file:$2">!;
' SCRAMToolBox/CMS/Configuration/CMSconfiguration
echo $PERL5LIB
echo rm -rf %i
mkdir -p $(dirname %i)

%{?buildarch:%buildarch}
%define realVersion %(echo %v | cut -f1 -d-)
perl -p -i -e 's|%{realVersion}([^-])|%{v}$1|g' %{bootstrapfile} 
cp -f %toolconf ./tmpconf
%if "%{cmsplatf}" == "%{gccwrapperarch}"
echo "Using gcc wrapper for %cmsplatf"
perl -p -i -e '$gccpath=$ENV{GCC_ROOT};$wrapperpath=$ENV{GCC_WRAPPER_ROOT};s|$gccpath|$wrapperpath|' ./tmpconf
%endif
scramv1 project -d $(dirname %i) -b %{bootstrapfile} -f ./tmpconf;
mv -f ./tmpconf %{i}/config/site

%build
pwd
# Remove cmt stuff that brings unwanted dependencies: 
rm -rf `find %{i}/src -type d -name cmt`
echo `scramv1 arch`
cd %i
echo %toolconf | sed 's|.*tools-||;s|.conf||' > config/site/sitename
cd src

%{?buildarch:%buildarch}

# Skip library checks to avoid dependency on seal:
export SCRAM_NOLOADCHECK=true
export SCRAM_NOSYMCHECK=true

if [ $(uname) = Darwin ]; then
  # scramv1 doesn't know the rpath variable on darwin...
  scramv1 b echo_null # ensure lib, bin exist
  eval `scramv1 runtime -sh`
  export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH
fi

%if "%{?preBuildCommand:set}" == "set"
echo "executing %preBuildCommand"
%preBuildCommand
%endif

%if "%{?buildtarget:set}" != "set"
%define buildtarget %{nil} 
%endif

#organize log file, turn off plugin building..
export BUILD_LOG yes
export SCRAM_NOPLUGINREFRESH yes

scramv1 b -r echo_CXX </dev/null
%if "%{?prebuildtarget:set}" == "set"
scramv1 b --verbose -f %{prebuildtarget} </dev/null
%endif
scramv1 b --verbose -f  %{compileOptions} %{makeprocesses} %{buildtarget} </dev/null
%if "%{?additionalBuildTarget0:set}" == "set"
scramv1 b --verbose -f %{additionalBuildTarget0} < /dev/null
%endif
%if "%{?postbuildtarget:set}" == "set"
scramv1 b --verbose -f %{postbuildtarget} </dev/null
%endif

rm -rf %i/tmp
chmod -R 755 %i %i/.SCRAM
(eval `scramv1 run -sh` ; SealPluginRefresh) || true
rm -fR %i/lib/%cmsplatf/.edmplugincache
(eval `scramv1 run -sh` ; EdmPluginRefresh) || true

%install
cd %i
%{?buildarch:%buildarch}
perl -p -i -e "s|^#!.*perl(.*)|#!/usr/bin/env perl$1|" $(grep -r -e "^#!.*perl.*" . | cut -d: -f1)
# need writeable directory for profile stuff
mkdir etc
yes | scramv1 install # FIXME: do by hand?

%post
%initenv
source $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/V1_0_3-p1/etc/profile.d/init.sh
cd $RPM_INSTALL_PREFIX/%cmsplatf/cms/%n/%v
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $(find config -type f) $(find .SCRAM -type f)
%{?buildarch:%buildarch}
yes | scramv1 install
(rm -rf external/%cmsplatf; ./config/linkexternal.pl --arch %cmsplatf --nolink INCLUDE) || true
