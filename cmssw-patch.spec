### RPM cms cmssw-patch CMSSW_5_3_11_patch4
Requires: cmssw-patch-tool-conf cms-git-tools
%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
