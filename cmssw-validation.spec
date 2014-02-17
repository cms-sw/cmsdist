### RPM cms cmssw-validation 1.0.0
BuildRequires: cmssw SCRAMV1 local-cern-siteconf
%define initenv	        %initenv_direct
#%define name1 1937
#%define moduleName LogParser
#%define url HTMLFiles/
#Source: svn://svn.cern.ch/reps/CMSIntBld/tags/LogParser/parser?scheme=svn+ssh&revision=%{name1}&module=%{moduleName}&output=/%{moduleName}.tar.gz
Source: svn://svn.cern.ch/reps/CMSIntBld/branches/degano/IntBuild?date=%realversion&scheme=svn+ssh&revision=HEAD&module=IntBuild&output=/IntBuild.tar.gz
Source1: fwlite_application_set
Source2: fwlite_build_set
Source3: online_application_set
Source4: online_build_set
Source5: das-cache

%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%setup -n IntBuild
cd ..
cp -r %_sourcedir/fwlite_application_set %_builddir/fwlite_application_set.file
cp -r %_sourcedir/fwlite_build_set       %_builddir/fwlite_build_set.file
cp -r %_sourcedir/online_application_set %_builddir/online_application_set.file
cp -r %_sourcedir/online_build_set       %_builddir/online_build_set.file
cp -r %_sourcedir/das-cache              %_builddir/das-cache.file
%build
cd $CMSSW_ROOT
eval `%scram runtime -sh`
%_builddir/IntBuild/IB/runTests.py --appset %_builddir
rm -rf %i/*
%install
# NOP

%post
# NOP
