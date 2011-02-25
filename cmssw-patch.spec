### RPM cms cmssw-patch CMSSW_3_11_1_hcalpatch1
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes

#use of diff config tag in order to build patch release
#without rebuilding full release
#this should go away when the fix is integratedin to full release too
%define configtag       V03-37-09-02

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
