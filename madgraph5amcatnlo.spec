### RPM external madgraph5amcatnlo 2.3.3
%define versiontag 2_3_3
Source: https://launchpad.net/mg5amcnlo/2.0/2.3.0/+download/MG5_aMC_v%{realversion}.tar.gz
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

# Remove all downloaded tgz files before building the package
find . -type f -name '*.tgz' -delete

%install
rsync -avh %{_builddir}/MG5_aMC_v%{versiontag}/ %{i}/
