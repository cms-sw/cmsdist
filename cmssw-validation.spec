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

# TODO: Add logs to the package or send them directly to the DB.
%install
# NOP

%post
# NOP
