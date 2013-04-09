### RPM cms cmssw-ib 1.0.0
BuildRequires: cmssw SCRAMV1 local-cern-siteconf python
%define initenv	        %initenv_direct
#%define name1 1937
#%define moduleName LogParser
#%define url HTMLFiles/
#Source: svn://svn.cern.ch/reps/CMSIntBld/tags/LogParser/parser?scheme=svn+ssh&revision=%{name1}&module=%{moduleName}&output=/%{moduleName}.tar.gz
Source: svn://svn.cern.ch/reps/CMSIntBld/trunk/IntBuild?scheme=svn+ssh&revision=HEAD&module=IntBuild&output=/IntBuild.tar.gz
%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%setup -n IntBuild
cd ..
%build
cd $CMSSW_ROOT
export CMSSW_VERSION
DOW=`$PYTHON_ROOT/bin/python -c "import os;from datetime import datetime;print datetime.strptime(os.environ['CMSSW_VERSION'].rsplit('_X_')[1], '%Y-%m-%d-%H00').strftime('%a').lower()"`
HOUR=`$PYTHON_ROOT/bin/python -c "import os;from datetime import datetime;print datetime.strptime(os.environ['CMSSW_VERSION'].rsplit('_X_')[1], '%Y-%m-%d-%H00').strftime('%H').lower()"`
eval `%scram runtime -sh`
CMSSW_MAJOR_MINOR=`echo $CMSSW_VERSION | sed -e 's/CMSSW_\([0-9]*\)_\([0-9]*\).*/\1.\2/g'`
%_builddir/IntBuild/IB/buildLogAnalyzer.py \
            -r $CMSSW_VERSION \
            -p $CMSSW_ROOT/src/PackageList.cmssw \
            --logDir %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION/logs/src \
            --topURL "http://cern.ch/cms-sdt/rc/%cmsplatf/www/$DOW/$CMSSW_MAJOR_MINOR-$DOW-$HOUR/new/"
rm -rf %i/*
%install
# NOP

%post
# NOP
