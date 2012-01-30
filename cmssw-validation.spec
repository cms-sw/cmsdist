### RPM cms cmssw-validation 1.0.0

Requires: cmssw SCRAMV1
Source: none

%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%scram project CMSSW $CMSSW_VERSION
cd $CMSSW_VERSION
%scram build clean
eval `%scram runtime -sh`
#rsync -av $CMSSW_RELEASE_BASE/src/ src/

%build
cd $CMSSW_VERSION
eval `%scram runtime -sh`
rm -rf test-addontests
mkdir test-addontests
cd test-addontests

BEGIN_TT=`date +%s`
addOnTests.py -j %compiling_processes &> result.log
END_TT=`date +%s`
DIFF_TT=$((END_TT - BEGIN_TT))

PASSED_TESTS=`cat result.log | awk '/tests passed/ { print $1 }'`
FAILED_TESTS=`cat result.log | awk '/tests passed/ { print $4 }'`

# TODO: Add logs to the package or send them directly to the DB.
%install
# NOP

%post
# NOP
