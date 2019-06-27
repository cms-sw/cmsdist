### RPM cms cmssw-dqm-reference-deployer CMSSW_6_0_0_pre11
## NOCOMPILER
%define defaultArch slc5_amd64_gcc462
Source0: http://cmsrep.cern.ch/cmssw/cms/RPMS/%{defaultArch}/cms+cmssw-dqm-reference-hi+%{realversion}-1-1.%{defaultArch}.rpm
Source1: http://cmsrep.cern.ch/cmssw/cms/RPMS/%{defaultArch}/cms+cmssw-dqm-reference-nonhi+%{realversion}-1-1.%{defaultArch}.rpm

%prep
%build
rm -rf %{_builddir}/data
cd %{_builddir}
for rpm in %{_sourcedir}/*.rpm; do
  dir=`basename $rpm`  
  mkdir -p data/$dir
  (cd data/$dir; rpm2cpio $rpm | cpio -idmv)
done
%install
mkdir %i/etc %i/data
touch %i/etc/runTheMatrix.args
for dir in `find %{_builddir}/data -name 'init.sh' -type f` ; do
  dir=`dirname $dir`/../..
  [ -d $dir/data ] || continue
  cp -r $dir/data/*HARVEST* %i/data
  [ -f $dir/etc/runTheMatrix.args ] && cat $dir/etc/runTheMatrix.args >> %i/etc/runTheMatrix.args
done
# bla bla
