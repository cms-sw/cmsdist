### RPM cms local-cern-siteconf sm111124
## NOCOMPILER

%define cmsrepo  cvs://:pserver:anonymous@cmscvs.cern.ch:2401/local/reps/CMSSW?passwd=AA_:yZZ3e
Source0: %{cmsrepo}&tag=-r%{realversion}&module=COMP/SITECONF/T1_CH_CERN&export=T1_CH_CERN&output=/T1_CH_CERN.tar.gz

%prep
%setup -T -b 0 -n T1_CH_CERN

%build
perl -p -i -e 's|\Q/afs/cern.ch/cms\E|%{i}|g' %{_builddir}/T1_CH_CERN/JobConfig/site-local-config.xml

%install
mkdir -p %i/SITECONF
cp -r %{_builddir}/T1_CH_CERN %i/SITECONF/T1_CH_CERN
ln -s T1_CH_CERN %i/SITECONF/local

%post
%{relocateConfig}/SITECONF/T1_CH_CERN/JobConfig/site-local-config.xml
if [ ! -d $RPM_INSTALL_PREFIX/SITECONF ] ; then 
  rm -f $RPM_INSTALL_PREFIX/SITECONF
  ln -s %{pkgrel}/SITECONF $RPM_INSTALL_PREFIX/SITECONF
fi
# bla bla
