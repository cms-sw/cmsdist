### RPM cms cmssw-validation 1.0.0
Requires: cmssw SCRAMV1
BuildRequires: local-cern-siteconf
%define name1 1827
%define moduleName LogParser
%define url HTMLFiles/
Source: svn://svn.cern.ch/reps/CMSIntBld/tags/LogParser/parser?scheme=svn+ssh&revision=%{name1}&module=%{moduleName}&output=/%{moduleName}.tar.gz


%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%setup -n %{moduleName}
cd ..
%scram project CMSSW $CMSSW_VERSION
cd $CMSSW_VERSION
%scram build clean
eval `%scram runtime -sh`
#rsync -av $CMSSW_RELEASE_BASE/src/ src/

%build
cd ..
cd $CMSSW_VERSION
eval `%scram runtime -sh`
rm -rf %i/test-addontests %i/test-runTheMatrix
mkdir -p %i/test-addontests %i/test-runTheMatrix
pushd %i/test-addontests
  time addOnTests.py -j %compiling_processes &> result.log
popd
cd ..
pwd
# Do runTheMatrix.py (let's start with -s)
pushd %i/test-runTheMatrix
  time runTheMatrix.py -s -j %compiling_processes &> result.log
popd
python %{moduleName}/parseLogs.py -f %i/test-runTheMatrix/runall-report-step123-.log -d  %{url}dbname.db -o %{url}tables.html &> parseLog.log

# TODO: Add logs to the package or send them directly to the DB.
%install
# NOP

%post
# NOP
