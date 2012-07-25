### RPM cms cmssw-dqm-reference-deployer CMSSW_5_2_5
## NOCOMPILER
%define defaultArch slc5_amd64_gcc462
Source: http://cmsrep.cern.ch/cmssw/cms/RPMS/%{defaultArch}/cms+cmssw-dqm-reference+%{realversion}-1-1.%{defaultArch}.rpm

%prep
%build
cd %{_builddir}
rpmFile=%{_sourcedir}/*.rpm
rpm2cpio $rpmFile | cpio -idmv

%install
mkdir %i/etc
cd %i
DQM_DATA_DIR=`find %{_builddir} -name "init.sh" -type f | head -n 1 | xargs dirname`
mv $DQM_DATA_DIR/../../data .
[ -f $DQM_DATA_DIR/../../etc/runTheMatrix.args ] && cp $DQM_DATA_DIR/../../etc/runTheMatrix.args etc/runTheMatrix.args
