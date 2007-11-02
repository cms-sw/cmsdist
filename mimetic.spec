### RPM external mimetic 0.8.9-CMS18
Source: http://codesink.org/download/%{n}-%{realversion}.tar.gz
Patch0: mimetic-0.8.9-gcc412

%prep
%setup -n %n-%{realversion}
%patch0 -p1

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
