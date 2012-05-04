### RPM cms cmssw-dqm-reference-deployer CMSSW_5_0_0
## NOCOMPILER
%define defaultArch slc5_amd64_gcc434
Source: http://cmsrep.cern.ch/cmssw/cms/RPMS/%{defaultArch}/cms+cmssw-dqm-reference+%{realversion}-1-1.%{defaultArch}.rpm

%prep
%build
cd %{_builddir}
rpmFile=%{_sourcedir}/*.rpm
rpm2cpio $rpmFile | cpio -idmv

%install
cd %i
DQM_DATA_DIR=`find %{_builddir} -name "init.sh" -type f | head -n 1 | xargs dirname`
mv $DQM_DATA_DIR/../../data .
