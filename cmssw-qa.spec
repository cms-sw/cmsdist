### RPM cms cmssw-validation 1.0.0
BuildRequires: cmssw SCRAMV1 local-cern-siteconf
%define initenv	        %initenv_direct
Source: svn://svn.cern.ch/reps/CMSIntBld/trunk/IntBuild?date=%(date +%%s)&scheme=svn+ssh&revision=HEAD&module=IntBuild&output=/IntBuild.tar.gz

%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%setup -n IntBuild
cd ..
%build
cd $CMSSW_ROOT
eval `%scram runtime -sh`
%_builddir/IntBuild/IB/runQA.py
rm -rf %i/*
%install
# NOP

%post
# NOP
# bla bla
