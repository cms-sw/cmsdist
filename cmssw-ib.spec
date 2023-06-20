### RPM cms cmssw-ib 2.0.0
## NO_AUTO_RUNPATH
## NO_VERSION_SUFFIX
BuildRequires: cmssw SCRAMV1
%define initenv	        %initenv_direct
%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf
Source: https://raw.githubusercontent.com/cms-sw/cms-bot/d68d86f103b7220765342a567d86b8aea42a4256/buildLogAnalyzer.py

%prep
%{?check_version_suffix:%check_version_suffix}
cd ..
%build
cd $CMSSW_ROOT
export CMSSW_VERSION
mkdir -p %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION
du -sh $CMSSW_ROOT/lib/%cmsplatf > %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION/library_size.txt
eval `%scram runtime -sh`
PYTHON_CMD=$(which python 2>/dev/null || echo python3)
DOW=`$PYTHON_CMD -c "import os;from datetime import datetime;print (datetime.strptime(os.environ['CMSSW_VERSION'].replace('_X_SLHC_', '_X_').rsplit('_X_')[1], '%Y-%m-%d-%H00').strftime('%a').lower())"`
HOUR=`$PYTHON_CMD -c "import os;from datetime import datetime;print (datetime.strptime(os.environ['CMSSW_VERSION'].replace('_X_SLHC_', '_X_').rsplit('_X_')[1], '%Y-%m-%d-%H00').strftime('%H').lower())"`

CMSSW_MAJOR_MINOR=`echo $CMSSW_VERSION | sed -e 's/CMSSW_\([0-9]*\)_\([0-9]*\).*/\1.\2/g'`
pushd %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION/logs/src
  cp -f src-logs.tgz $(echo $CMSSW_ROOT | sed 's|%cmsroot/|%cmsroot/BUILD/|')/src-logs.tgz
  tar xzf src-logs.tgz
popd
cp %{_sourcedir}/buildLogAnalyzer.py $CMSSW_ROOT/buildLogAnalyzer.py
$PYTHON_CMD $CMSSW_ROOT//buildLogAnalyzer.py \
            -r $CMSSW_VERSION \
            -p $CMSSW_ROOT/src/PackageList.cmssw \
            --logDir %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION/logs/src \
            --topURL "http://cern.ch/cms-sdt/rc/%cmsplatf/www/$DOW/$CMSSW_MAJOR_MINOR-$DOW-$HOUR/new/"

cd %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION/logs/html
zip -r ../html-logs.zip ./
cd ..
rm -rf src html
mkdir -p html
mv html-logs.zip html

rm -rf %i/*
%install
# NOP

%post
# NOP
