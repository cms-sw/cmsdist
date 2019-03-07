### RPM cms cmssw-patch CMSSW_9_4_13_patch1
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define saveDeps        yes
# build with debug symbols, and package them in a separate rpm
%define subpackageDebug yes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}
%if "%(case %realversion in (*_ICC_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_ICC_X.*|_X|')
%define gitcommit       %(echo %realversion | sed -e 's|_ICC_X|_X|')
%define scram_compiler  icc
%define extra_tools     icc-cxxcompiler icc-f77compiler icc-ccompiler
%endif

%if "%(case %realversion in (*_CLANG_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_CLANG_X.*|_X|')
%define gitcommit       %(echo %realversion | sed -e 's|_CLANG_X|_X|')
%define scram_compiler  llvm
%define extra_tools     llvm-cxxcompiler llvm-f77compiler llvm-ccompiler
%endif

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
