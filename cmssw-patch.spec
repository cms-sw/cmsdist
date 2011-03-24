### RPM cms cmssw-patch CMSSW_4_1_3_patch2
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

# use a different config tag in order to build patch release without rebuilding the full release
# this should go away when the fix is integratedin to full release
%define configtag       V03-40-05-01

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
