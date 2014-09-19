### RPM cms cmssw-ib 1.0.0
BuildRequires: cmssw SCRAMV1 local-cern-siteconf python
%define initenv	        %initenv_direct
Source: git://github.com/cms-sw/int-build.git?date=%(date +%%Y%%m%%d%%H%%M)&obj=master/HEAD&export=IntBuild&output=/int-build-%{realversion}.tgz
%define scram $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

%prep
%setup -n IntBuild
cd ..
%build
cd $CMSSW_ROOT
export CMSSW_VERSION
mkdir -p %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION
du -sh $CMSSW_ROOT/lib/%cmsplatf > %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION/library_size.txt
PYTHON_CMD="$PYTHON_ROOT/bin/python"
case %cmsplatf in
  *_mic_*)
    PYTHON_CMD="/usr/bin/python"
  ;;
esac
DOW=`$PYTHON_CMD -c "import os;from datetime import datetime;print datetime.strptime(os.environ['CMSSW_VERSION'].replace('_X_SLHC_', '_X_').rsplit('_X_')[1], '%Y-%m-%d-%H00').strftime('%a').lower()"`
HOUR=`$PYTHON_CMD -c "import os;from datetime import datetime;print datetime.strptime(os.environ['CMSSW_VERSION'].replace('_X_SLHC_', '_X_').rsplit('_X_')[1], '%Y-%m-%d-%H00').strftime('%H').lower()"`
eval `%scram runtime -sh`
CMSSW_MAJOR_MINOR=`echo $CMSSW_VERSION | sed -e 's/CMSSW_\([0-9]*\)_\([0-9]*\).*/\1.\2/g'`
pushd %cmsroot/WEB/build-logs/%cmsplatf/$CMSSW_VERSION/logs/src
  tar xzf src-logs.tgz
popd
$PYTHON_CMD %_builddir/IntBuild/IB/buildLogAnalyzer.py \
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
