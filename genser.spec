### RPM lcg genser GENSER_1_4_1-CMS3q
## IMPORT configurations 
Requires: genser-tool-conf
Patch0: genser

%define patchsrc2 perl -p -i -e "s/slc4_ia32_gcc34/slc4_ia32_gcc345/;s/slc4_amd64_gcc34/slc4_amd64_gcc345/" %configtree/RequirementsDoc %configtree/BuildFile
%define patchsrc3 perl -p -i -e 's!<select name=root>!!' %{configtree}/RequirementsDoc ; 

%define confversion %lcgConfiguration 
%define toolconf ${GENSER_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf
%define patchsrc %%patch0
%define cvsdir simu
%define cvsserver simu 
%define cvsproj GENSER
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsconfig simu/GENSER/config/scram
%define isGenser true
%define UseSPI   true

%define srctree1 pythia/6_227
%define pythiaversion pythia-6227-0
%define additionalSrc0 cvs://:pserver:anonymous@simu.cvs.cern.ch:2401/cvs/simu?passwd=Ah<Z&tag=-r%{pythiaversion}&module=simu/GENSER/pythia&export=%{srctree1}

%define toprexversion toprex-421-0
%define srctree2 toprex/421
%define additionalSrc1 cvs://:pserver:anonymous@simu.cvs.cern.ch:2401/cvs/simu?passwd=Ah<Z&tag=-r%{toprexversion}&module=simu/GENSER/toprex&export=%{srctree2}


%define tauolaversion tauola-27-121-1
%define srctree3 tauola/27.121.1
%define additionalSrc2 cvs://:pserver:anonymous@simu.cvs.cern.ch:2401/cvs/simu?passwd=Ah<Z&tag=-r%{tauolaversion}&module=simu/GENSER/tauola&export=%{srctree3}

%define charybdis charybdis-1002-0
%define srctree4 charybdis/1_002
%define additionalSrc3 cvs://:pserver:anonymous@simu.cvs.cern.ch:2401/cvs/simu?passwd=Ah<Z&tag=-r%{charybdis}&module=simu/GENSER/charybdis&export=%{srctree4}

%define photos   photos-215-1
%define srctree5 photos/215
%define additionalSrc4 cvs://:pserver:anonymous@simu.cvs.cern.ch:2401/cvs/simu?passwd=Ah<Z&tag=-r%{photos}&module=simu/GENSER/photos&export=%{srctree5}

%define herwig herwig-6510-2
%define srctree6 herwig/6_510
%define additionalSrc5 cvs://:pserver:anonymous@simu.cvs.cern.ch:2401/cvs/simu?passwd=Ah<Z&tag=-r%{herwig}&module=simu/GENSER/herwig&export=%{srctree6}

%define additionalSubst s!cvs:[?]module=simu/GENSER/config/scram!file:config!;

%define buildtarget release
%define conflevel %{nil}
%define buildtarget %{nil} 

%define bootstrapfile %_builddir/%{configtree}/BootStrapFile
%define scrambuildcmd rm -rf pythia/6_227/examples; scram b lib ; cd pythia/6_227/dummy ; scram b lib ; cd ../pdfdummy ; scram b lib ; cd ../../../toprex/421 ; scram b lib; cd ../../tauola/27.121.1; scram b lib; cd aux1; scram b; cd ..; cd ../../charybdis/1_002; scram b lib  ; cd ../../photos/215; scram b lib; cd ../../herwig/6_510; scram b lib; cd dummy; scram b lib; cd ../pdfdummy; scram b lib

## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scram-build

