### RPM lcg roofit 5.24.00
%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://root.cern.ch/svn/root/tags/v%svnTag/roofit?scheme=http&module=roofit&output=/roofit.tgz

Patch:  roofit-5.24-00-build.sh 
Patch1: root-5.22-00a-roofit-silence-static-printout

Requires: root 

%prep
%setup -n roofit
%patch -p1
%patch1 -p2
 
%build
chmod +x build.sh
./build.sh

%install
mv build/lib %i/
mkdir %i/include
cp -r build/inc/* %i/include

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d

# rootroofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootroofit
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootroofit version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=TMVA>
<use name=ROOTMLP>
<use name=rootminuit>
</Tool> 
EOF_TOOLFILE

# rootroostats toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootroostats
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootroostats version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=TMVA>
<use name=ROOTMLP>
<use name=rootminuit>
</Tool> 
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/rootroofit
%{relocateConfig}etc/scram.d/rootroostats
