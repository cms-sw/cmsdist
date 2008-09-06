### RPM external millepede 2.0
# CAREFUL: NO VERSION IN TARBALL !!!
# Source: http://www.desy.de/~blobel/Mptwo.tgz
Source: http://cmsrep.cern.ch/cmssw/millepede-mirror/millepede-2.0.tar.gz

Patch: millepede_2008_08_18
Patch1: millepede_64bit_2008_08_18

%prep
%setup -n millepede-%realversion
%patch -p1

%if "%cpu" == "amd64"
%patch1 -p1
%endif

%build
make %makeprocesses

%install
make install
mkdir -p %i/bin
cp bin/* %i/bin

# Toolfile with only PATH
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# millepede tool file
cat << \EOF_TOOLFILE >%i/etc/scram.d/millepede
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=millepede version=%v>
<info url="http://www.desy.de/~blobel"></info>
<Client>
 <Environment name=MILLEPEDE_BASE default="%i"></Environment>
</Client>
<use name=sockets>
<use name=pcre>
<use name=zlib>
<Runtime name=PATH value="$MILLEPEDE_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n


