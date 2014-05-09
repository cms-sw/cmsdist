### RPM cms cmssw CMSSW_7_1_X_2014-04-24-0200

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

%if "%(case %realversion in (*_EXPERIMENTAL_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_EXPERIMENTAL_X.*|_X|')
%define usercxxflags    -O3 -ffast-math -freciprocal-math -fipa-pta
%endif

%if "%(case %realversion in (*_FORTIFIED_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define usercxxflags    -fexceptions -fstack-protector-all --param=ssp-buffer-size=4
%endif

%if "%(case %realversion in (*_ICC_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define preBuildCommand scram setup icc-cxxcompiler ; scram setup icc-f77compiler ; scram setup icc-ccompiler ; export COMPILER=icc
%endif

%if "%(case %realversion in (*_BOOSTIO_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_X.*|_X|')
%define preBuildCommand scram setup boost_serialization; scram setup boost_iostreams
%endif

%if "%(case %realversion in (*_THREADED_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define branch		%(echo %realversion | sed -e 's|_X.*|_X|')
%endif

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
