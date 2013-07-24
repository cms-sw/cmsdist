### RPM cms cmssw CMSSW_5_3_11
Requires: cmssw-tool-conf python

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes
%define branch          CMSSW_5_3_X
%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{realversion}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

# Build with clang if _CLANG_X is in the name of the package.
%if "%(case %realversion in (*_CLANG_X*) echo true ;; (*) echo false ;; esac)" == "true"
Patch10: cmssw-clang
Patch20: cmssw-clang-vla
%define cvstag		%(echo %realversion | sed -e 's|_CLANG_X|_X|')
%define preBuildCommand pushd .. ; patch -p1 <%_sourcedir/cmssw-clang ; popd ; patch -p0 <%_sourcedir/cmssw-clang-vla & true
%define buildtarget     checker
%endif

# This clang build has also the multithreading checkers enabled.
%if "%(case %realversion in (*_CLANGMT_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_CLANGMT_X|_X|')
%define buildtarget     checker
%endif

%if "%(case %realversion in (*_EXPERIMENTAL_X*) echo true ;; (*) echo false ;; esac)" == "true"
Patch11: cmssw-experimental
Patch20: cmssw-drop-isnan
%define cvstag		%(echo %realversion | sed -e 's|_EXPERIMENTAL_X|_X|')
%define preBuildCommand pushd .. ; patch -p1 <%_sourcedir/cmssw-experimental ; popd ; patch -p0 <%_sourcedir/cmssw-drop-isnan & true
%endif

%if "%(case %realversion in (*_COVERAGE_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_COVERAGE_X|_X|')
%define usercxxflags    -fprofile-arcs -ftest-coverage
%endif

%if "%(case %realversion in (*_FORTIFIED_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_FORTIFIED_X|_X|')
%define usercxxflags    -fexceptions -fstack-protector-all --param=ssp-buffer-size=4
%endif

%if "%(case %realversion in (*_LTO_X*) echo true ;; (*) echo false ;; esac)" == "true"
Patch12: cmssw-lto
%define cvstag		%(echo %realversion | sed -e 's|_LTO_X|_X|')
%define preBuildCommand pushd .. ; patch -p1 <%_sourcedir/cmssw-lto ; popd
%endif

%if "%(case %realversion in (*_DEBUG_X*) echo true ;; (*) echo false ;; esac)" == "true"
Patch13: cmssw-debug
%define cvstag		%(echo %realversion | sed -e 's|_DEBUG_X|_X|')
%define preBuildCommand pushd .. ; patch -p1 <%_sourcedir/cmssw-debug; popd
%endif

%if "%(case %realversion in (*_ICC_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_ICC_X|_X|')
%define preBuildCommand export COMPILER=icc
%endif

%if "%(case %realversion in (*_ASAN_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_ASAN_X|_X|')
%define usercxxflags    -fsanitize=address -fno-omit-frame-pointer -g 
%endif

## IMPORT scram-project-build
