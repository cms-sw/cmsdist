### RPM cms cmssw-validation 1.0.0
Requires: cmssw SCRAMV1
BuildRequires: local-cern-siteconf
%define name1 1937
%define moduleName LogParser
%define url HTMLFiles/
Source: svn://svn.cern.ch/reps/CMSIntBld/tags/LogParser/parser?scheme=svn+ssh&revision=%{name1}&module=%{moduleName}&output=/%{moduleName}.tar.gz

# Template spec file for implementing IB tasks.
# Execute your test (runTheMatrix.py in this case) and copy all of what 
# you want to expose to the user into %cmsroot/WEB/$CMSSW_VERSION/
# This will be automatically uploaded to the repository in the WEB area.
%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%setup -n %{moduleName}
cd ..
%scram project CMSSW $CMSSW_VERSION
cd $CMSSW_VERSION
%scram build clean
eval `%scram runtime -sh`

%build
cd ..
cd $CMSSW_VERSION
UPLOAD_AREA=%cmsroot/WEB/ib-results/$CMSSW_VERSION
TEST_AREA=%i/workarea
eval `%scram runtime -sh`
rm -rf $TEST_AREA
mkdir -p $TEST_AREA
mkdir -p $UPLOAD_AREA
pushd $TEST_AREA
  time runTheMatrix.py -l 1000 -j %compiling_processes 2>&1 >$UPLOAD_AREA/result.log
popd
rm -rf $TEST_AREA
#python %{moduleName}/parseLogs.py -f %i/test-runTheMatrix/runall-report-step123-.log -d  %{url}dbname.db -o %{url}tables.html -v $CMSSW_VERSION &> parseLog.log 

# TODO: Add logs to the package or send them directly to the DB.
%install
# NOP

%post
# NOP
