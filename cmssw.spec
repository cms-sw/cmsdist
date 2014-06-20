### RPM cms cmssw CMSSW_5_3_19
Requires: cmssw-tool-conf python cms-git-tools

%define runGlimpse yes
%define useCmsTC yes
%define saveDeps yes
%define branch CMSSW_5_3_X
%define gitcommit %{realversion}

%if "%(case %realversion in (*_ICC_X*) echo true ;; (*) echo false ;; esac)" == "true"
Patch99: cmssw-5.3.X-icc
%define gitcommit %(echo %realversion | sed -e 's|_ICC_X|_X|')
%define preBuildCommand scram setup mpfr; scram setup gmp; scram setup icc-cxxcompiler ; scram setup icc-f77compiler ; scram setup icc-ccompiler
%define patchsrc9       cat %_sourcedir/cmssw-5.3.X-icc | patch -s -p0 --fuzz=0
%endif

%define source1 git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
