### RPM external mimetic 0.9.5
Source: http://codesink.org/download/%{n}-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i
make

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=mimetic version=%v>
<lib name=mimetic>
<Client>
 <Environment name=MIMETIC_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$MIMETIC_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$MIMETIC_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
