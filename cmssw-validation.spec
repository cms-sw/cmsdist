### RPM cms cmssw-validation 1.0.0
BuildRequires: cmssw SCRAMV1 local-cern-siteconf
%define initenv	        %initenv_direct
Source: git://github.com/cms-sw/int-build.git?date=%(date +%%Y%%m%%d%%H%%M)&obj=master/HEAD&export=IntBuild&output=/int-build-%{realversion}.tgz
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
# On systems which support it, abort builds after 11.5h
case %cmsplatf in 
  osx*) TIMEOUT= ;;
  *) TIMEOUT="timeout 39630" ;;
esac
eval `%scram runtime -sh`
$TIMEOUT %_builddir/IntBuild/IB/runTests.py --appset %_builddir || true
rm -rf %i/*
%install
# NOP

%post
# NOP
