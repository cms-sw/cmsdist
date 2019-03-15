### RPM cms cmssw CMSSW_7_1_38

Requires: cmssw-tool-conf python cms-git-tools

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes
%define branch          CMSSW_7_0_X
%define gitcommit       %{realversion}

%if "%(case %realversion in (*_COVERAGE_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_COVERAGE_X.*|_X|')
%define usercxxflags    -fprofile-arcs -ftest-coverage
%endif

%if "%(case %realversion in (*_DEBUG_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_DEBUG_X.*|_X|')
%define gitcommit       %(echo %realversion | sed -e 's|_DEBUG||')
%endif

%if "%(case %realversion in (*_EXPERIMENTAL_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_EXPERIMENTAL_X.*|_X|')
%define usercxxflags    -O3 -ffast-math -freciprocal-math -fipa-pta
%endif

%if "%(case %realversion in (*_FORTIFIED_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define usercxxflags    -fexceptions -fstack-protector-all --param=ssp-buffer-size=4
%endif

%if "%(case %realversion in (*_ICC_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_ICC_X.*|_X|')
%define preBuildCommand scram setup icc-cxxcompiler ; scram setup icc-f77compiler ; scram setup icc-ccompiler ; perl -p -i -e 's|<client>|<client><flags DEFAULT_COMPILER="icc"/>|' %i/config/Self.xml; export COMPILER=icc ;
%endif

%if "%(case %realversion in (*_CLANG_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_CLANG_X.*|_X|')
%define preBuildCommand scram setup llvm-cxxcompiler ; scram setup llvm-f77compiler ; scram setup llvm-ccompiler ; perl -p -i -e 's|<client>|<client><flags DEFAULT_COMPILER="llvm"/>|' %i/config/Self.xml ; export COMPILER=llvm ;
%endif

%if "%(case %realversion in (*_BOOSTIO_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_X.*|_X|')
%endif

%if "%(case %realversion in (*_THREADED_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_X.*|_X|')
%endif

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
