### RPM external madgraph5_amcatnlo 2.2.3
%define versiontag 2_2_3
Source: https://launchpad.net/mg5amcnlo/2.0/2.2.0/+download/MG5_aMC_v%{realversion}.tar.gz
Patch0: madgraph5amcatnlo-config

Requires: python 
Requires: hepmc
# Further requirements are more or less optional, however, convenient
Requires: pythia8
Requires: herwigpp
Requires: lhapdf
Requires: fastjet
%prep
%setup -n MG5_aMC_v%{versiontag}

%patch0 -p1 

%build

%install

