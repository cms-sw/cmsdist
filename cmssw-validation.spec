### RPM cms cmssw-validation 1.0.0
Requires: cmssw SCRAMV1
BuildRequires: local-cern-siteconf
Source: none

%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%scram project CMSSW $CMSSW_VERSION
cd $CMSSW_VERSION
%scram build clean
eval `%scram runtime -sh`
#rsync -av $CMSSW_RELEASE_BASE/src/ src/

%build

# keep this for the DB regression tests below
topDir=`pwd`

cd $CMSSW_VERSION
eval `%scram runtime -sh`
rm -rf %i/test-addontests %i/test-runTheMatrix
mkdir -p %i/test-addontests %i/test-runTheMatrix

pushd %i/test-addontests
  time addOnTests.py -j %compiling_processes &> result.log
popd

# Do runTheMatrix.py (let's start with -s)
pushd %i/test-runTheMatrix
  time runTheMatrix.py -s -j %compiling_processes &> result.log
popd

# Run the CondCore regression tests
rm -rf %i/dbRegTests
mkdir -p %i/dbRegTests
pushd %i/dbRegTests
	exePath=$topDir/$CMSSW_VERSION/src/CondCore/RegressionTest/python/
   	# needed for now, to be moved to a python file and imported:
	cp $exePath/sequences.xml .
	# logs here are just in case something goes wrong with uploading them to the DB:
	for rt in ORA ExportIOV; do
		python $exePath/run_regression.py --full -t $rt"_regression" -r $CMSSW_VERSION -a $SCRAM_ARCH -p $topDir -w &>full_$rt.log
		python $exePath/run_regression.py --self -t $rt"_regression" -r $CMSSW_VERSION -a $SCRAM_ARCH -p $topDir -w &>self_$rt.log
	done
popd


# TODO: Add logs to the package or send them directly to the DB.
%install
# NOP

%post
# NOP
