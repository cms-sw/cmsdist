### RPM cms cmssw-dqm-reference CMSSW_5_3_0
## NOCOMPILER
BuildRequires: cmssw
BuildRequires: local-cern-siteconf
Source: none
%define initenv %initenv_direct
%define RunTheMatrixArgs  --useInput all --command '-n 200'
%prep
%build
cmssw_ver=`echo $CMSSW_VERSION | sed 's|-cms\d*$||'`
if [ "$cmssw_ver" != "%{realversion}" ] ; then
  echo "ERROR: %n version %realversion does not match with cmssw version $cmssw_ver"
  echo "       Please update %n.spec file and use $cmssw_ver as its version"
  exit 1
fi

source %{cmsroot}/cmsset_default.sh
CMS_PATH=$LOCAL_CERN_SITECONF_ROOT; export CMS_PATH
cd $CMSSW_ROOT
eval `scram run -sh`

cd %_builddir
rm -rf pyRelval
mkdir pyRelval
cd pyRelval
wfs=`runTheMatrix.py -n | grep '^[0-9][0-9]*\.[0-9][0-9]*  *.*+HARVEST' | awk '{print $1}' | tr '\n' ',' | sed 's|,$||'`
runTheMatrix.py %{RunTheMatrixArgs} -l $wfs -j 8

%install
mkdir %i/data
wfs=""
for dir in `find  %{_builddir}/pyRelval -name "*+HARVEST*" -maxdepth 1 -mindepth 1 -type d` ; do
  dname=`basename $dir`
  for file in `find $dir -name "DQM_V*.root" -type f`; do
    [ -d %i/data/$dname ] || mkdir %i/data/$dname
    cp $file %i/data/$dname
    wfs="$wfs `echo $dname | sed -e s'|_.*||'`"
  done
done
if [ "X$wfs" != "X" ] ; then
  mkdir %i/etc
  wfs=`echo $wfs | tr ' ' '\n' | sort | uniq | tr '\n' ',' | sed 's|,$||'`
  echo "%{RunTheMatrixArgs} -l $wfs" > %i/etc/runTheMatrix.args
fi
