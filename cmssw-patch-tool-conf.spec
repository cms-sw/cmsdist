### RPM cms cmssw-patch-tool-conf 3.0
# with cmsBuild, change the above version only when a new
# tool is added

## NOCOMPILER
## INSTALL_DEPENDENCIES cmsLHEtoEOSManager gcc-fixincludes

Requires: cmssw-toolfile

# still need this (from the non-patch tool-conf spec ...
%define skipreqtools jcompiler

## INCLUDE scramv1-tool-conf
