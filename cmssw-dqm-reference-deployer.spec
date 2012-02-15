### RPM cms cmssw-dqm-reference-deployer CMSSW_5_0_0
## NOCOMPILER
Source: http://cmsrep.cern.ch/cms/cpt/Software/download/cms/RPMS/slc5_amd64_gcc434/cms+cmssw-dqm-reference+CMSSW_5_0_0-1-1.slc5_amd64_gcc434.rpm
%define initenv %initenv_direct

%prep
%build
%install
rpmFile=%{_sourcedir}/*.rpm
rpm2cpio $rpmFile | cpio -idmv

DQM_DATA_DIR=`find . -name "data" | head -n 1`
COPY_FROM_DIR=$DQM_DATA_DIR/../../../../../`ls $DQM_DATA_DIR/../../../../../`

cp -r $COPY_FROM_DIR $CMS_PATH
