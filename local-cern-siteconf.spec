### RPM cms local-cern-siteconf sm111124
## NOCOMPILER
%define cmsrepo  cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source0: %{cmsrepo}&tag=-r%{realversion}&module=COMP/SITECONF/T1_CH_CERN&export=T1_CH_CERN&output=/T1_CH_CERN.tar.gz

%prep 
rm -rf T1_CH_CERN
%setup -T -b 0 -n T1_CH_CERN

%build
perl -p -i -e 's|\Q/afs/cern.ch/cms\E|%{i}|g' %{_builddir}/T1_CH_CERN/JobConfig/*

%install
cd %i
mkdir -p SITECONF
cp -r %{_builddir}/T1_CH_CERN SITECONF/T1_CH_CERN
ln -s T1_CH_CERN SITECONF/local

%post
%{relocateConfig}/SITECONF/T1_CH_CERN/JobConfig/site-local-config.xml
