### RPM external madgraph5_amcatnlo 2.3.0.beta
%define versiontag 2_3_0_beta
Source: https://launchpad.net/mg5amcnlo/2.0/2.2.0/+download/MG5_aMC_v%{realversion}.tar.gz
Patch0: madgraph5amcatnlo-config

Requires: python 
Requires: hepmc
%prep
%setup -n MG5_aMC_v%{versiontag}

%patch0 -p1 

%build

%install
rsync -avh %{_builddir}/MG5_aMC_v%{versiontag}/ %{i}/
