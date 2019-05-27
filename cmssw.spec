### RPM cms cmssw CMSSW_10_2_15

Requires: cmssw-tool-conf python cms-git-tools

%define runGlimpse      yes
%define saveDeps        yes
%define branch          master
%define gitcommit       %{realversion}
# build with debug symbols, and package them in a separate rpm
%define subpackageDebug yes

%if "%(case %realversion in (*_COVERAGE_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define usercxxflags    -fprofile-arcs -ftest-coverage
%endif

%if "%(case %realversion in (*_DEBUG_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define gitcommit       %(echo %realversion | sed -e 's|_DEBUG_X|_X|')
%endif

%if "%(case %realversion in (*_EXPERIMENTAL_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define usercxxflags    -O3 -ffast-math -freciprocal-math -fipa-pta
%endif

%if "%(case %realversion in (*_FORTIFIED_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define usercxxflags    -fexceptions -fstack-protector-all --param=ssp-buffer-size=4 -Wp,-D_FORTIFY_SOURCE=2
%endif

%if "%(case %realversion in (*_ICC_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define gitcommit       %(echo %realversion | sed -e 's|_ICC_X|_X|')
%define scram_compiler  icc
%define extra_tools     mpfr gmp icc-cxxcompiler icc-f77compiler icc-ccompiler
%endif

%if "%(case %realversion in (*_CLANG_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define scram_compiler  llvm
%define extra_tools     llvm-cxxcompiler llvm-f77compiler llvm-ccompiler
%endif

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
