### RPM external doxygen 1.5.4
Source: http://ftp.stack.nl/pub/users/dimitri/%n-%realversion.src.tar.gz
#Patch0: doxygen
#Patch1: doxygen-1.4.1-gcc412
Requires: graphviz

%prep

%setup -n %n-%realversion
#%ifos darwin
#%patch0 -p1
#%endif
#%patch1 -p1

%build
./configure --prefix %i --dot $GRAPHVIZ_ROOT/bin/dot
make %makeprocesses

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=doxygen version=%v>
<Client>
 <Environment name=DOXYGEN_BASE default="%i"></Environment>
</Client>
<Runtime name=PATH value="$DOXYGEN_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
