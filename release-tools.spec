### RPM cms release-tools 1.0

%define cvstag V00-01-01
%define moduleName Utilities/ReleaseScripts
%define exportName ReleaseScripts
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/ReleaseScripts.tar.gz
Requires: p5-template-toolkit p5-dbi

%prep
%setup -n ReleaseScripts
%build
%install
mkdir -p %{i}/bin
cp -r ReleaseScripts/scripts/* %{i}/bin 
ln -sf %{i}/etc/profile.d/init.sh  %{instroot}/%{cmsplatf}/etc/profile.d/S00release-tools.sh
ln -sf %{i}/etc/profile.d/init.csh %{instroot}/%{cmsplatf}/etc/profile.d/S00release-tools.csh
ln -sf %{i}/inst-files %{instroot}/inst-files

%files
%{i}
%{instroot}/%{cmsplatf}/etc/profile.d/S00release-tools.sh
%{instroot}/%{cmsplatf}/etc/profile.d/S00release-tools.csh

%post
ln -sf $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh  $RPM_INSTALL_PREFIX/%cmsplatf/etc/profile.d/S00release-tools.sh
ln -sf $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh $RPM_INSTALL_PREFIX/%cmsplatf/etc/profile.d/S00release-tools.csh
