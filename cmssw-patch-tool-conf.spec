### RPM cms cmssw-patch-tool-conf CMSSW_6_2_0_SLHC23
# with cmsBuild, change the above version only when a new
# tool is added

Requires: cmssw-toolfile

# still need this (from the non-patch tool-conf spec ...
%define skipreqtools jcompiler lhapdfwrapfull lhapdffull cuda opencl opencl-cpp

## IMPORT scramv1-tool-conf
