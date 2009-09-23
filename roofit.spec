### RPM lcg roofit 5.24.00
%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://root.cern.ch/svn/root/tags/v%svnTag/roofit?scheme=http&module=roofit&output=/roofit.tgz

Patch:  roofit-5.24-00-build.sh 
Patch1: root-5.22-00a-roofit-silence-static-printout
Patch2: roofit-5.24-00-RooFactoryWSTool-include

Requires: root 

%prep
%setup -n roofit
%patch -p1
%patch1 -p2
%patch2 -p1
 
%build
chmod +x build.sh
# Remove an extra -m64 from Wouter's build script
perl -p -i -e 's|-m64 ||' build.sh
./build.sh

%install
mv build/lib %i/
mkdir %i/include
cp -r build/inc/* %i/include

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d

# rootroofitcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootroofitcore
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootroofitcore version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=RooFitCore>
<use name=rootcore>
<use name=roothistmatrix>
<use name=rootgpad>
<use name=rootminuit>
<Client>
 <Environment name=ROOFIT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$ROOFIT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$ROOFIT_BASE/include"></Environment>
</Client>
</Tool> 
EOF_TOOLFILE

# rootroofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootroofit
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootroofit version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=RooFit>
<use name=rootroofitcore>
<use name=rootcore>
<use name=roothistmatrix>
</Tool> 
EOF_TOOLFILE

# rootroostats toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootroostats
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootroostats version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=RooStats>
<use name=rootroofitcore>
<use name=rootroofit>
<use name=rootcore>
<use name=roothistmatrix>
<use name=rootgpad>
</Tool> 
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/rootroofitcore
%{relocateConfig}etc/scram.d/rootroofit
%{relocateConfig}etc/scram.d/rootroostats
