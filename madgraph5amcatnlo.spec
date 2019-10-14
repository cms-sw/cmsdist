### RPM external madgraph5amcatnlo 2.6.7
%define versiontag 2_6_7
%define commit 307
Provides: perl(Compress::Zlib)
Provides: perl(List::Util)
Source: http://cmsrep.cern.ch/cmssw/download/%{n}-%{realversion}.tgz
#Source: https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/MG5_aMC_v%{realversion}.tar.gz
#Source: https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v%{realversion}.tar.gz
Patch0: madgraph5amcatnlo-config

Requires: python
Requires: hepmc
# Needed for ExRoot analysis package
Requires: root   
# Needed for Syscalc package
Requires: lhapdf
Requires: gosamcontrib
Requires: fastjet
Requires: pythia8
Requires: thepeg
                   
%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

sed -i -e "s|\${HEPMC_ROOT}|${HEPMC_ROOT}|g" input/.mg5_configuration_default.txt
sed -i -e "s|\${PYTHIA8_ROOT}|${PYTHIA8_ROOT}|g" input/.mg5_configuration_default.txt
sed -i -e "s|\${LHAPDF_ROOT}|${LHAPDF_ROOT}|g" input/.mg5_configuration_default.txt
sed -i -e "s|\${FASTJET_ROOT}|${FASTJET_ROOT}|g" input/.mg5_configuration_default.txt
sed -i -e "s|\${GOSAMCONTRIB_ROOT}|${GOSAMCONTRIB_ROOT}|g" input/.mg5_configuration_default.txt
sed -i -e "s|\${THEPEG_ROOT}|${THEPEG_ROOT}|g" input/.mg5_configuration_default.txt
sed -i -e "s|@MADGRAPH5AMCATNLO_ROOT@|%{i}|g" input/.mg5_configuration_default.txt

%build
export FC="$(which gfortran) -std=legacy"

# Start small NLO event generation to make sure that all additional packages are compiled
cat <<EOF > basiceventgeneration.txt
generate p p > t t~ [QCD]
output basiceventgeneration
launch
set nevents 5
EOF
./bin/mg5_aMC ./basiceventgeneration.txt

# Remove all downloaded tgz files before building the package
find . -type f -name '*.tgz' -delete

%install
rsync -avh %{_builddir}/%{n}-%{realversion}/ %{i}/
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' \
    %{i}/Template/LO/bin/internal/addmasses_optional.py \
    %{i}/madgraph/various/progressbar.py
find %{i} -name '*deleteme' -delete

%post
%{relocateConfig}input/.mg5_configuration_default.txt
