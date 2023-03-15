### RPM cms cmssw CMSSW_13_1_0_pre1_LossyCompression

Requires: cmssw-tool-conf

%define runGlimpse      yes
%define saveDeps        yes
%define branch          master
%define gitcommit       %{realversion}
# build with debug symbols, and package them in a separate rpm
#subpackage debug disabledes

## INCLUDE cmssw-queue-override

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## SUBPACKAGE debug IF %subpackageDebug
## INCLUDE scram-project-build
