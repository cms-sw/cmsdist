### RPM configuration cern 1.0
# Example file for site specific configurations.

%define sitename %n
%define cvstag HEAD
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=COMP/SITECONFIG/%{sitename}&export=SITECONFIG&tag=-r%{cvstag}&output=/SITECONFIG.tar.gz

%prep
%build
%install
mkdir -p %instroot/SITECONFIG/%{sitename}/JobConfig
mkdir -p %instroot/SITECONFIG/%{sitename}/PhEDEx

cp %{_sourcedir}/SITECONFIG/%{sitename}/JobConfig/site-local-config.xml %{instroot}/SITECONFIG/%{sitename}/JobConfig/site-local-config.xml
cp %{_sourcedir}/SITECONFIG/%{sitename}/PhEDEx/storage.xml %{instroot}/SITECONFIG/%n/PhEDEx/storage.xml

%post
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|" SITECONFIG/%{sitename}/storage.xml SITECONFIG/%{sitename}/site-local.xml
ln -sf $RPM_INSTALL_PREFIX/SITECONF/%{sitename} $RPM_INSTALL_PREFIX/SITECONF/local
%files
%instroot/SITECONFIG/%n
