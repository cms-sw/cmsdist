### RPM cms cmssw-patch CMSSW_3_11_1_patch1
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

%if "%(case %realversion in (*_ICC_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_ICC_X.*|_X|')
%define preBuildCommand scram setup icc-cxxcompiler ; scram setup icc-f77compiler ; scram setup icc-ccompiler ; perl -p -i -e 's|<client>|<cliend>\n<flags DEFAULT_COMPILER="icc"/>|' %i/config/Self.xml
%endif

%if "%(case %realversion in (*_CLANG_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_CLANG_X.*|_X|')
%define preBuildCommand scram setup llvm-cxxcompiler ; scram setup llvm-f77compiler ; scram setup llvm-ccompiler ; perl -p -i -e 's|<client>|<cliend>\n<flags DEFAULT_COMPILER="llvm"/>|' %i/config/Self.xml
%endif

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
