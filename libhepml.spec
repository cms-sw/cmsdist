### RPM external libhepml 0.2.1
Source: http://mcdb.cern.ch/distribution/api/%{n}-%{realversion}.tar.gz

%prep
%setup -q -n %{n}-%{realversion}

%build
cd src
make
mv *.so ../lib/.

%install
tar -c lib interface | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=libhepml version=%v>
<Client>
 <Environment name=LIBHEPML_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LIBHEPML_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$LIBHEPML_BASE/interface"></Environment>
</Client>
<lib name=libhepml>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
