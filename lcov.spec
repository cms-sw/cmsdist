### RPM external lcov 1.6
Source: http://heanet.dl.sourceforge.net/sourceforge/ltp/%n-%realversion.tar.gz
Patch0: lcov-merge-files-in-same-dir

%prep
%setup -n %n-%realversion
%patch0 -p1

%build
make %makeprocesses

%install
make PREFIX=%i install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=lcov version=%v>
<Client>
 <Environment name=LCOV_BASE default="%i"></Environment>
</Client>
<Runtime name=PATH value="$LCOV_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
