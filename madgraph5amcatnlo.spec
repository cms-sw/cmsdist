### RPM external madgraph5amcatnlo 2.4.3
%define versiontag 2_4_3
Provides: perl(Compress::Zlib)
Provides: perl(List::Util)
Source: https://launchpad.net/mg5amcnlo/2.0/2.4.x/+download/MG5_aMC_v%{realversion}.tar.gz
Patch0: madgraph5amcatnlo-config
# Compile and install internal and external packages
Patch1: madgraph5amcatnlo-compile    

Requires: python
Requires: hepmc
# Needed for ExRoot analysis package
Requires: root   
# Needed for Syscalc package
Requires: lhapdf
                   
%prep
%setup -n MG5_aMC_v%{versiontag}

%patch0 -p1
%patch1 -p1

%build

# Save patched config
cp input/mg5_configuration.txt input/mg5_configuration_patched.txt

# Compile in advance
chmod +x bin/compile.py
./bin/compile.py
# Remove compile script after compilation
rm bin/compile.py

# Add back patched config after compilation since its get overwritten
# Save patched config
mv input/mg5_configuration_patched.txt input/mg5_configuration.txt

# Start small NLO event generation to make sure that all additional packages are compiled
cat <<EOF > basiceventgeneration.txt
generate p p > t t~ [QCD]
output basiceventgeneration
launch
set nevents 100
EOF
./bin/mg5_aMC ./basiceventgeneration.txt

# Remove folder of basic event generation
rm -rf basiceventgeneration

# Remove all downloaded tgz files before building the package
find . -type f -name '*.tgz' -delete

%install
rsync -avh %{_builddir}/MG5_aMC_v%{versiontag}/ %{i}/
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' \
    %{i}/Template/LO/bin/internal/addmasses_optional.py \
    %{i}/madgraph/various/progressbar.py
find %{i} -name '*deleteme' -delete
