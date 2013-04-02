### RPM cms cmssw-mic CMSSW_6_2_0_pre4
Requires: cmssw-mic-tool-conf

Patch10: cmssw-icc
%define ucprojtype      CMSSW
%define source1         cvs://:pserver:anonymous@cmscvs.cern.ch:2401/local/reps/CMSSW?passwd=AA_:yZZ3e&tag=-r%{realversion}&module=Utilities/Timing&export=src/Utilities&output=/src.tar.gz
%define preBuildCommand pushd .. ; patch -p1 <%_sourcedir/cmssw-icc ; popd

## IMPORT scram-project-build
